#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""App Management

Usage:
    manage.py pep8
    manage.py translate

Arguments:
    pep8        Run pep8 linting on source
    translate   Scan source for translations and create/update necessary
                .po[t] files

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

    if opt['translate']:
        from app.management import translate
        translate.run()
