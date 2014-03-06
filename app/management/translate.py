# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import subprocess

from app import app

EXTRACT_COMMAND = "pybabel extract -F babel.cfg " \
                  "-k lazy_gettext -o app/translations/messages.pot app"

INIT_COMMAND = "pybabel init -i app/translations/messages.pot " \
               "-d app/translations"

UPDATE_COMMAND = "pybabel update -i app/translations/messages.pot " \
                 "-d app/translations"

COMPILE_COMMAND = "pybabel compile -d app/translations"


def run():
    # Scan source to extract any changes to translated text to messages.pot
    print "Running {}".format(EXTRACT_COMMAND)
    subprocess.check_call(EXTRACT_COMMAND.split())

    for lang in app.config['LANGUAGES']:
        print
        # If the language .po file already exists, just run pybabel update
        if os.path.isfile(os.path.join(
            'app', 'translations', lang, 'LC_MESSAGES', 'messages.po'
        )):
            update_command = UPDATE_COMMAND + ' -l {}'.format(lang)
            print "Running {}".format(update_command)
            subprocess.check_call(update_command.split())

        # Otherwise, run pybabel init to create a new .po
        else:
            init_command = INIT_COMMAND + ' -l {}'.format(lang)
            print "Running {}".format(init_command)
            subprocess.check_call(init_command.split())

    # Finally, try to compile the language files
    print
    print "Running {}".format(COMPILE_COMMAND)
    content = subprocess.check_output(
        COMPILE_COMMAND.split(), stderr=subprocess.STDOUT
    )

    print content

    if 'fuzzy' in content:
        print """
            Some translation files above were marked fuzzy, you should manually
            correct these and re-run manage.py translate
        """
