#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""App Management

Usage:
    manage.py check
    manage.py test [-d | --debug] [-c | --coverage]
    manage.py pep8
    manage.py requirements
    manage.py translate
    manage.py db reset [--clean] [--head]
    manage.py db update <message>
    manage.py db upgrade [<revision>] [-x | --execute]
    manage.py db downgrade <revision> [-x | --execute]

Arguments:
    check               Run tests and pep8 (use to verify before commit)
    test                Run tests
        -d --debug      Disable output capture, and drop to PDB on exception
        -c --coverage   Run test coverage
    pep8                Run pep8 linting on source
    requirements        Updates requirements.txt with pip freeze
    translate           Scan source for translations and create/update necessary
                        .po[t] files
    db                  Database management
        reset           Reset and populate the database (local db only)
            --clean     Don't populate new database with test data
            --head      Bump alembic head revision to current database schema
        update          Run alembic auto-revision check for changed schema
            <message>   Revision message
        upgrade         Output schema upgrade plan to <revision> (default most recent)
        downgrade       Output schema downgrade plan to <revision>
        -x --execute    Execute the schema migration plan

Options:
    -h --help           Show this

 """
from __future__ import unicode_literals

from docopt import docopt

if __name__ == '__main__':
    opt = docopt(__doc__)

    if opt['test'] or opt['check']:
        from app.management import test
        test.run(debug=opt['--debug'], coverage=opt['--coverage'])

    if opt['pep8'] or opt['check']:
        from app.management import pep8
        pep8.run()

    if opt['translate']:
        from app.management import translate
        translate.run()

    if opt['db']:
        from app.management import db

        if opt['reset']:
            db.reset(clean=opt['--clean'], head=opt['--head'])

        elif opt['update']:
            db.update(message=opt['<message>'])

        elif opt['upgrade']:
            db.upgrade(
                revision=opt['<revision>'] or 'head',
                execute=opt['--execute'],
            )

        elif opt['downgrade']:
            db.downgrade(
                revision=opt['<revision>'],
                execute=opt['--execute'],
            )

    if opt['requirements']:
        from app.management import requirements
        requirements.run()
