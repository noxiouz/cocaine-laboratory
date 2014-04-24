#!/usr/bin/env python
import logging

from cocaine.logging import LoggerHandler
from cocaine.worker import Worker

from converter import NashvilleFilter
from converter import GothamFilter
from converter import ToasterFilter
from converter import LomoFilter
from converter import KelvinFilter

log = logging.getLogger("cocagram")
log.addHandler(LoggerHandler())
log.setLevel(logging.DEBUG)


def do(fltr):
    def applyfilter(request, response):
        content = yield request.read()
        data = fltr().apply(content)
        response.write(data)
        response.close()
    return applyfilter


if __name__ == "__main__":
    w = Worker()
    w.run({"KelvinFilter": do(KelvinFilter),
           "NashvilleFilter": do(NashvilleFilter),
           "ToasterFilter": do(ToasterFilter),
           "GothamFilter": do(GothamFilter),
           "LomoFilter": do(LomoFilter)})
