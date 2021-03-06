#! python
#! coding: utf-8

import os
import yaml
from unidecode import unidecode

_thisLoc = os.path.dirname(__file__)
_entityTypes = yaml.load(open(os.path.join(_thisLoc, "../resources", "entityTypes.yaml"), "r"))
_puncToCollapse = yaml.load(open(os.path.join(_thisLoc, "../resources", "puncToCollapse.yaml"), "r"))
_puncToRemove = yaml.load(open(os.path.join(_thisLoc, "../resources", "puncToRemove.yaml"), "r"))
_puncToReplace = yaml.load(open(os.path.join(_thisLoc, "../resources", "puncToReplace.yaml"), "r"))

# seperate out single token and multi-token entities for faster processing
_multiToken = {}
_singleToken = {}

for _e in _entityTypes:
    if " " in _e:
        _multiToken[_e] = _entityTypes[_e]
    else:
        _singleToken[_e] = _entityTypes[_e]


def _collapseAbbrv(_s):
    """ helper method used to collapse abbreviations like "a b c" to "abc"
        returns list of tokens for efficiency in normalize method
    """
    _t = ""
    _a = []
    for x in _s.split(" "):
        if len(x) == 1:
            _t = _t + x
        else:
            if len(_t) > 0:
                _a.append(_t)
                _t = ""
            _a.append(x)
    if len(_t) > 0:
        _a.append(_t)
    return _a


def normalize(org):
    """ primary method used to normalize an org name
        accepts: organization name
        returns: normalized org name

        assumes that the user wants shortest strings possible, which is helpful when
        computing edit distance between two strings. therefore incorporated is shortened
        to inc rather than inc being expanded to incorporated.

    """
    if org is None: return None
    for x in _puncToCollapse: org = org.replace(x, '')
    for x in _puncToRemove: org = org.replace(x, ' ')
    org = unidecode(org).lower().strip()
    org = " ".join([_puncToReplace[x] if x in _puncToReplace else x for x in org.split(" ")])  # replace synonyms
    org = " ".join([_singleToken[x] if x in _singleToken else x for x in _collapseAbbrv(org)])  # replace synonyms
    for x in _entityTypes:  # replace multi token phrases
        org = org.replace(x, _entityTypes[x])
    return " ".join(org.split())  # removes any multiples of white space in middle of strings
