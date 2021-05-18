# @Author: Lampros.Karseras
# @Date:   06/01/2021 22:58
import pkgutil
import techniques
import logging
from importlib import import_module
import attr

logger = logging.getLogger(__name__)


def getAllTechniques():
    found_techniques = []
    for importer, modname, ispkg in pkgutil.walk_packages(path=techniques.__path__, prefix=techniques.__name__ + '.',
                                                          onerror=lambda x: None):
        if not ispkg:
            found_techniques.append(modname)

    loaded_techniques = []
    for technique in found_techniques:
        technique_module = import_module(technique)
        loaded_techniques.append(technique_module)
        # TODO: Validate techniques

    return (
        {technique.TECH_ID: technique for technique in loaded_techniques}
    )


@attr.s(frozen=True)
class parameters:
    input = attr.ib()
    output = attr.ib()
