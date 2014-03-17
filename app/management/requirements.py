# -*- coding: utf-8 -*-
""" Runs `pip freeze > requirements.txt`, excluding some development
packages (see `EXCLUDE_PACKAGES`)
"""
from __future__ import unicode_literals

import subprocess
import os

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

REQUIREMENTS_FILE = "requirements.txt"

REQUIREMENTS_PATH = os.path.join(BASEDIR, REQUIREMENTS_FILE)

COMMAND = "pip freeze > {}".format(REQUIREMENTS_PATH)

EXCLUDE_PACKAGES = {
    # IPython
    'ipython',

    # pdb++
    'pdbpp',
    'fancycompleter',
    'wmctrl',
    'Pygments',
    'pyrepl',
}


def run():
    print "Running {}\n".format(COMMAND)
    requirements_in = subprocess.check_output(
        COMMAND.split(),
        stderr=subprocess.STDOUT
    )

    if not 'Flask' in requirements_in:
        return

    with open(REQUIREMENTS_PATH, 'w') as requirements_out:
        requirements_out.writelines(
            line + '\n' for line in requirements_in.splitlines()
            if not any(package in line for package in EXCLUDE_PACKAGES)
        )

