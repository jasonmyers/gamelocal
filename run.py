#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from app import app, webassets


def run():
    # Tell webassets to not minify js/css in debug mode
    webassets.debug = True

    app.run(debug=True)


if __name__ == '__main__':
    run()

