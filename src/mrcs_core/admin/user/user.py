"""
Created on 29 Nov 2025

@author: Bruno Beloff (bbeloff@me.com)

A structured representation of a user

{
  "uid": "c69a665c-11b5-4755-a903-97095f9dc915",
  "email": "bbeloff@me.com",
  "role": "ADMIN",
  "must_set_password": true,
  "given_name": "Bruno",
  "family_name": "Beloff",
  "created": "2025-11-30T09:36:23.553+00:00",
  "latest_login": null
}
"""

from collections import OrderedDict
from enum import unique, StrEnum

from mrcs_core.data.datum import Datum
from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONable
from mrcs_core.data.meta_enum import MetaEnum


# --------------------------------------------------------------------------------------------------------------------

@unique
class UserRole(StrEnum, metaclass=MetaEnum):
    """
    An enumeration of all the possible user roles
    """

    ADMIN = 'ADMIN'
    DESIGNER = 'DESIGNER'
    OPERATOR = 'OPERATOR'
    OBSERVER = 'OBSERVER'


# --------------------------------------------------------------------------------------------------------------------

class User(JSONable):
    """
    a structured representation of a user
    """

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        email = jdict.get('email')

        if not Datum.is_email_address(email):
            raise ValueError(f'{email} is not a valid email')

        uid = jdict.get('uid')
        email = email
        role = UserRole(jdict.get('role'))                      # may raise ValueError
        must_set_password = jdict.get('must_set_password')
        given_name = jdict.get('given_name')
        family_name = jdict.get('family_name')
        created = ISODatetime.construct_from_jdict(jdict.get('created'))
        latest_login = ISODatetime.construct_from_jdict(jdict.get('latest_login'))

        return cls(uid, email, role, must_set_password, given_name, family_name, created, latest_login)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uid: str | None, email: str, role: UserRole, must_set_password: bool,
                 given_name: str, family_name: str, created: ISODatetime | None, latest_login: ISODatetime | None):
        super().__init__()

        self.__uid = uid
        self.__email = email
        self.__role = role
        self.__must_set_password = must_set_password
        self.__given_name = given_name
        self.__family_name = family_name
        self.__created = created
        self.__latest_login = latest_login


    def __eq__(self, other):
        try:
            return self.uid == other.uid
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other):
        if self.family_name < other.family_name:
            return True

        if self.family_name > other.family_name:
            return False

        if self.given_name < other.given_name:
            return True

        if self.given_name > other.given_name:
            return False

        return self.email < other.email


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['uid'] = self.uid
        jdict['email'] = self.email
        jdict['role'] = str(self.role)
        jdict['must_set_password'] = self.must_set_password
        jdict['given_name'] = self.given_name
        jdict['family_name'] = self.family_name
        jdict['created'] = self.created
        jdict['latest_login'] = self.latest_login

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def uid(self):
        return self.__uid


    @property
    def email(self):
        return self.__email


    @property
    def role(self):
        return self.__role


    @property
    def must_set_password(self):
        return self.__must_set_password


    @property
    def given_name(self):
        return self.__given_name


    @property
    def family_name(self):
        return self.__family_name


    @property
    def created(self):
        return self.__created


    @property
    def latest_login(self):
        return self.__latest_login


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{uid:{self.uid}, email:{self.email}, role:{self.role}, '
                f'must_set_password:{self.must_set_password}, given_name:{self.given_name}, '
                f'family_name:{self.family_name}, created:{self.created}, latest_login:{self.latest_login}}}')
