#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""App Management

Usage:
    manage.py check
    manage.py test [-d | --debug]
    manage.py pep8
    manage.py translate
    manage.py db reset
    manage.py db update <message>
    manage.py db upgrade [<revision>]
    manage.py db downgrade <revision>

Arguments:
    check               Run tests and pep8 (use to verify before commit)
    test                Run tests
        -d --debug      Disable output capture, and drop to PDB on exception
    pep8                Run pep8 linting on source
    translate           Scan source for translations and create/update necessary
                        .po[t] files
    db                  Database management
        reset           Reset and populate the database (local db only)
        update          Run alembic auto-revision check for changed schema
            <message>   Revision message
        upgrade         Upgrade the database schema
            <revision>  Upgrade to which revision (default most recent)
        downgrade       Downgrade the database schema to revision
            <revision>  Downgrade to which revision

Options:
    -h --help   Show this

 """
from __future__ import unicode_literals

from docopt import docopt

if __name__ == '__main__':
    opt = docopt(__doc__)

    if opt['test'] or opt['check']:
        from app.management import test
        test.run(debug=opt['--debug'])

    if opt['pep8'] or opt['check']:
        from app.management import pep8
        pep8.run()

    if opt['translate']:
        from app.management import translate
        translate.run()

    if opt['db']:
        from app.management import db

        if opt['reset']:
            db.reset()

        elif opt['update']:
            db.update(message=opt['<message>'])

        elif opt['upgrade']:
            db.upgrade(revision=opt['<revision>'] or 'head')

        elif opt['downgrade']:
            db.downgrade(revision=opt['<revision>'])
