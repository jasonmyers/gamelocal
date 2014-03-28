# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nose
import subprocess


def run(debug=False, coverage=False):
    argv = ['nosetests', '-w', 'tests', '--logging-clear-handlers']
    if debug:
        argv += ['-v', '-s', '--debug', '--pdb', '--pdb-failure',
                 '--nocapture', '--nologcapture']

    if coverage:
        argv += ['--with-coverage', '--cover-package=app',
                 '--cover-erase', '--cover-tests', '--cover-branches',
                 '--cover-html']

    print "Running {}\n".format(" ".join(argv))

    subprocess.Popen(argv).communicate()
