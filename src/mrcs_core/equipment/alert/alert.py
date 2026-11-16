"""
Created on 15 Nov 2026

@author: Bruno Beloff (bbeloff@me.com)

An alert object, raised when an unexpected event occurs

{
    "type": "Alert",
    "id": null,
    "severity": "HIGH",
    "impact": "GLOBAL",
    "subject": "TRACK",
    "text": "short happened",
    "raised": "2026-11-15T08:43:56.970+00:00",
    "resolved": null
}
"""

from collections import OrderedDict
from typing import Any, Self

from mrcs_core.data.iso_datetime import ISODatetime
from mrcs_core.data.json import JSONable
from mrcs_core.equipment.alert.alert_enums import Impact, Severity, Subject


# --------------------------------------------------------------------------------------------------------------------

class Alert(JSONable):
    """
    an alert object, raised when an unexpected event occurs
    """


    @classmethod
    def construct(cls, severity: Severity, impact: Impact, subject: Subject, text: str) -> Self:
        return cls(None, severity, impact, subject, text, ISODatetime.now(), None)


    @classmethod
    def construct_from_jdict(cls, jdict) -> Self:
        type_name = jdict.get('type')

        if type_name != 'Alert':
            raise TypeError(f'required type:{cls.type_name()} got:{type_name}')

        id = None if jdict.get('id') is None else int(jdict.get('id'))

        severity = Severity[jdict.get('severity')]  # may raise KeyError
        impact = Impact(jdict.get('impact'))
        subject = Subject(jdict.get('subject'))

        text = jdict.get('text')

        raised_at = ISODatetime.construct_from_jdict(jdict.get('raised'))
        resolved_at = ISODatetime.construct_from_jdict(jdict.get('resolved'))

        return cls(id, severity, impact, subject, text, raised_at, resolved_at)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, id: int | None, severity: Severity, impact: Impact, subject: Subject, text: str,
                 raised_at: ISODatetime, resolved_at: ISODatetime | None):
        self.__id = id
        self.__severity = severity
        self.__impact = impact
        self.__subject = subject
        self.__text = text
        self.__raised_at = raised_at
        self.__resolved_at = resolved_at


    def __eq__(self, other: Any) -> bool:
        try:
            return (self.id == other.id and self.severity == other.severity and self.impact == other.impact and
                    self.subject == other.subject and self.text == other.text and self.raised_at == other.raised_at and
                    self.resolved_at == other.resolved_at)
        except (AttributeError, TypeError):
            return False


    def __lt__(self, other: Any) -> bool:
        return self.raised_at < other.raised_at


    # ----------------------------------------------------------------------------------------------------------------

    # TODO: the type may be reported as PersistentAlert, which could be problematic - override tyoe_name()
    # TODO: check all the Persistent classes

    def as_json(self, **kwargs):
        jdict = OrderedDict()

        jdict['type'] = self.type_name()

        jdict['id'] = self.id
        jdict['severity'] = self.severity
        jdict['impact'] = self.impact
        jdict['subject'] = self.subject
        jdict['text'] = self.text
        jdict['raised'] = self.raised_at
        jdict['resolved'] = self.resolved_at

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def has_id(self) -> bool:
        return self.id is not None


    @property
    def is_resolved(self) -> bool:
        return self.resolved_at is not None


    def resolve(self):
        if self.is_resolved:
            raise RuntimeError('attempt to resolve an alert that is already resolved')

        self.__resolved_at = ISODatetime.now()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def id(self):
        return self.__id


    @property
    def severity(self):
        return self.__severity


    @property
    def impact(self):
        return self.__impact


    @property
    def subject(self):
        return self.__subject


    @property
    def text(self):
        return self.__text


    @property
    def raised_at(self):
        return self.__raised_at


    @property
    def resolved_at(self):
        return self.__resolved_at


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return (f'{self.__class__.__name__}:{{id:{self.id}, severity:{self.severity}, impact:{self.impact}, '
                f'subject:{self.subject}, text:{self.text}, raised_at:{self.raised_at}, '
                f'resolved_at:{self.resolved_at}}}')
