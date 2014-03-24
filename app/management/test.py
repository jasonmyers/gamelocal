# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nose


def run(debug=False):
    argv = ['-w', 'tests', '--logging-clear-handlers']
    if debug:
        argv += ['-v', '-s', '--debug', '--pdb', '--pdb-failure',
                 '--nocapture', '--nologcapture']

    print "Running nosetests {}\n".format(" ".join(argv))
    nose.run(argv=argv)
