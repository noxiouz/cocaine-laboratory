#!/usr/bin/env python
from cocaine.worker import Worker
from cocaine.decorators.wsgi import wsgi

from app import app

W = Worker()

W.run({"http": wsgi(app)})
