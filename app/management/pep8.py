# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess

COMMAND = "pep8 --statistics --show-source app/"


def run():
    subprocess.Popen(COMMAND.split()).communicate()
