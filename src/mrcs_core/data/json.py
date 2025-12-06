"""
Created on 13 Aug 2016

@author: Bruno Beloff (bbeloff@me.com)

JSONify must handle **kw because the standard JSONEncoder does not.

https://stackoverflow.com/questions/42568262/how-to-encrypt-text-with-a-password-in-python
"""

import json
import os
import time

from abc import abstractmethod, ABC
from decimal import Decimal

from mrcs_core.data.datum import Datum


# --------------------------------------------------------------------------------------------------------------------

class JSONify(json.JSONEncoder):
    """
    classdocs
    """

    @classmethod
    def as_jdict(cls, obj, **kwargs):
        if isinstance(obj, JSONable):
            return cls.as_jdict(obj.as_json(**kwargs))

        if isinstance(obj, dict):
            return {key: cls.as_jdict(value, **kwargs) for key, value in obj.items()}

        if isinstance(obj, list):
            return tuple(cls.as_jdict(value, **kwargs) for value in obj)

        return obj


    @staticmethod
    def dumps(obj, skipkeys=False, ensure_ascii=False, check_circular=True,
              allow_nan=True, cls=None, indent=None, separators=None,
              default=None, sort_keys=False, **kwargs):

        handler = JSONify if cls is None else cls

        return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                          allow_nan=allow_nan, cls=handler, indent=indent, separators=separators,
                          default=default, sort_keys=sort_keys, **kwargs)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *, skipkeys=False, ensure_ascii=True,
                 check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None, **kwargs):

        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                         check_circular=check_circular, allow_nan=allow_nan, sort_keys=sort_keys,
                         indent=indent, separators=separators, default=default)

        self.__kwargs = kwargs


    # ----------------------------------------------------------------------------------------------------------------

    def default(self, obj):
        if isinstance(obj, JSONable):
            return obj.as_json(**self.__kwargs)

        if isinstance(obj, Decimal):
            return float(obj) if Datum.is_float(str(obj)) else int(obj)

        return json.JSONEncoder.default(self, obj)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'JSONify:{{kwargs:{self.__kwargs}}}'


# --------------------------------------------------------------------------------------------------------------------

class JSONable(ABC):
    """
    classdocs
    """

    _INDENT = 4

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def loads(cls, jstr):
        if not jstr:
            return None

        try:
            return json.loads(jstr)
        except json.decoder.JSONDecodeError:
            raise ValueError(jstr.strip())


    # ----------------------------------------------------------------------------------------------------------------

    def as_list(self, jlist):
        del jlist[:]                                    # empty the list

        for key, value in self.as_json().items():
            try:
                value = value.as_json()
            except AttributeError:
                pass

            jlist.append((key, value))                  # append the key-value pairs of the dictionary


    # ----------------------------------------------------------------------------------------------------------------

    def as_jdict(self, **kwargs):
        return JSONify.as_jdict(self, **kwargs)


    @abstractmethod
    def as_json(self, **kwargs):
        pass


# --------------------------------------------------------------------------------------------------------------------

class JSONReport(JSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, filename, skeleton=False):
        if filename is None:
            return None

        if not os.path.isfile(filename):
            return cls.construct_from_jdict(None, skeleton=skeleton)

        with open(filename) as f:
            return cls.construct_from_jdict(json.load(f), skeleton=skeleton)


    @classmethod
    def delete(cls, filename):
        if filename is None:
            return

        os.remove(filename)


    # noinspection PyUnusedLocal
    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        return cls()


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, filename):
        if filename is None:
            return None

        # data...
        jstr = JSONify.dumps(self, indent=self._INDENT)

        # file...
        tmp_filename = '.'.join((filename, str(int(time.time()))))

        try:
            with open(tmp_filename, 'w') as f:
                f.write(jstr + '\n')

        except FileNotFoundError:           # the containing directory does not exist (yet)
            return False

        # atomic operation...
        os.rename(tmp_filename, filename)

        return True


# --------------------------------------------------------------------------------------------------------------------

class JSONCatalogueEntry(JSONReport, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def list(cls):
        return tuple(cls.__filename_to_name(item) for item in sorted(os.listdir(cls.catalogue_location()))
                     if item.endswith('.json'))


    @classmethod
    def exists(cls, name):
        return name in cls.list()


    @classmethod
    def retrieve(cls, name):
        return cls.load(cls.__catalogue_entry_location(name))


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def catalogue_location(cls):
        return ''


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __catalogue_entry_location(cls, name):
        return os.path.join(cls.catalogue_location(), cls.__name_to_filename(name))


    @classmethod
    def __name_to_filename(cls, name):
        return name.replace('.', '-') + '.json'


    @classmethod
    def __filename_to_name(cls, name):
        return name.replace('-', '.')[:-len('.json')]


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filename(self):
        return self.__catalogue_entry_location(self.name)


    # ----------------------------------------------------------------------------------------------------------------

    def store(self):
        self.save(self.filename)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def name(self):
        pass


# --------------------------------------------------------------------------------------------------------------------

class AbstractPersistentJSONable(JSONable, ABC):
    """
    classdocs
    """

    _SECURITY_DELAY =       3.0                                 # seconds

    __AWS_DIR =             "aws"                               # hard-coded rel path
    __CONF_DIR =            "conf"                              # hard-coded rel path

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def aws_dir(cls):
        return cls.__AWS_DIR


    @classmethod
    def conf_dir(cls):
        return cls.__CONF_DIR


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, last_modified=None):
        self._last_modified = last_modified                     # LocalizedDatetime


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def save(self, manager):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def last_modified(self):
        return self._last_modified


# --------------------------------------------------------------------------------------------------------------------

class PersistentJSONable(AbstractPersistentJSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def exists(cls, manager):
        try:
            dirname, filename = cls.persistence_location()
        except NotImplementedError:
            return False

        return manager.exists(dirname, filename)


    @classmethod
    def load(cls, manager, encryption_key=None, skeleton=False):
        if not cls.exists(manager):
            return cls.construct_from_jdict(None, skeleton=skeleton)

        try:
            dirname, filename = cls.persistence_location()
        except NotImplementedError:
            return None

        try:
            jstr, last_modified = manager.load(dirname, filename, encryption_key=encryption_key)
        except (KeyError, ValueError) as ex:            # caused by incorrect encryption_key
            time.sleep(cls._SECURITY_DELAY)
            raise ex

        try:
            obj = cls.construct_from_jdict(cls.loads(jstr), skeleton=skeleton)
            obj._last_modified = last_modified
            return obj

        except (AttributeError, TypeError):
            return None


    @classmethod
    def delete(cls, manager):
        try:
            dirname, filename = cls.persistence_location()
            manager.remove(dirname, filename)

        except NotImplementedError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict, skeleton=False):
        pass


    @classmethod
    @abstractmethod
    def persistence_location(cls):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        self._last_modified = None                          # last_modified field shall be restored by load(..)

        dirname, filename = self.persistence_location()
        jstr = JSONify.dumps(self, indent=self._INDENT)

        manager.save(jstr, dirname, filename, encryption_key=encryption_key)


# --------------------------------------------------------------------------------------------------------------------

class MultiPersistentJSONable(AbstractPersistentJSONable, ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def list(cls, manager):
        try:
            dirname, filename = cls.persistence_location(None)
        except NotImplementedError:
            return None

        suffix_len = len(filename) + 1
        items = manager.list(manager.scs_path(), dirname)

        return tuple(item[:-suffix_len] for item in items if item.endswith(filename))


    @classmethod
    def exists(cls, manager, name=None):
        try:
            dirname, filename = cls.persistence_location(name)
        except NotImplementedError:
            return False

        return manager.exists(dirname, filename)


    @classmethod
    def load(cls, manager, name=None, encryption_key=None, skeleton=False):
        if not cls.exists(manager, name=name):
            return cls.construct_from_jdict(None, name=name, skeleton=skeleton)

        try:
            dirname, filename = cls.persistence_location(name)
        except NotImplementedError:
            return None

        try:
            jstr, last_modified = manager.load(dirname, filename, encryption_key=encryption_key)

        except (KeyError, ValueError) as ex:            # caused by incorrect encryption_key
            time.sleep(cls._SECURITY_DELAY)
            raise ex

        try:
            obj = cls.construct_from_jdict(cls.loads(jstr), name=name, skeleton=skeleton)
            obj._last_modified = last_modified
            return obj

        except (AttributeError, TypeError):
            return None


    @classmethod
    def delete(cls, manager, name=None):
        try:
            dirname, filename = cls.persistence_location(name)
            manager.remove(dirname, filename)

        except NotImplementedError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, jdict, name=None, skeleton=False):
        pass


    @classmethod
    @abstractmethod
    def persistence_location(cls, name):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name, last_modified=None):
        super().__init__(last_modified=last_modified)

        self.__name = name                                  # string


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, manager, encryption_key=None):
        self._last_modified = None                          # last_modified field shall be restored by load(..)

        dirname, filename = self.persistence_location(self.name)
        jstr = JSONify.dumps(self, indent=self._INDENT)

        manager.save(jstr, dirname, filename, encryption_key=encryption_key)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MultiPersistentJSONable:{name:%s}" % self.name
