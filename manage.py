# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""App Management

Usage:
    manage.py pep8

Arguments:
    pep8        Run pep8 linting on source

Options:
    -h --help   Show this

 """
from __future__ import unicode_literals

from docopt import docopt

if __name__ == '__main__':
    opt = docopt(__doc__)

    if opt['pep8']:
        from app.management import pep8
        pep8.run()
