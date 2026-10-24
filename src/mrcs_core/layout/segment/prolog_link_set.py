"""
Created on 18 Oct 2026

@author: Bruno Beloff (bbeloff@me.com)

Translation between prolog and python segments
"""

from typing import Any

from mrcs_core.layout.segment.prolog_link import PrologLink
from mrcs_core.layout.segment.segment_location import SegmentLocation


# --------------------------------------------------------------------------------------------------------------------

class LinkSetKey(object):
    """
    the key for the LinkSet dictionary
    """


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, start: SegmentLocation, end: SegmentLocation):
        self.__start = start
        self.__end = end


    def __eq__(self, other: Any) -> bool:
        return self.start == other.start and self.end == other.end


    def __hash__(self):
        return hash((self.start, self.end))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def start(self):
        return self.__start


    @property
    def end(self):
        return self.__end


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return f'LinkSetKey:{{start:{self.start}, end:{self.end}}}'


# --------------------------------------------------------------------------------------------------------------------

class LinkSet(object):
    """
    A set of link assertions
    """


    @classmethod
    def construct(cls):
        return cls({})


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, links: dict[LinkSetKey, PrologLink]):
        self.__links = links


    def __eq__(self, other: Any) -> bool:
        try:
            return self.links == other.links
        except (AttributeError, TypeError):
            return False


    def __len__(self):
        return len(self.__links)


    # ----------------------------------------------------------------------------------------------------------------

    def add(self, link: PrologLink):
        key = LinkSetKey(link.location, link.next_location)

        if key not in self.__links:
            self.__links[key] = link
            return

        self.__links[key].add(*link.constraints)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def links(self):
        return list(self.__links.values())


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        links = '{' + ', '.join(f'{key}: {link}' for key, link in self.__links.items())
        return f'PrologLinkSet:{{links:{links}}}'
