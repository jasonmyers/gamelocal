# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nose


def run(debug=False):
    argv = ['-w', 'tests']
    if debug:
        argv += ['-v', '-s', '--debug',
                 '--nocapture', '--nologcapture', '--pdb']

    print "Running nosetests {}\n".format(" ".join(argv))
    nose.run(argv=argv)
