# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import bs4

from app import app


def send_email(to, subject, html):

    if app.config['DEBUG']:
        print 'To: ', to
        print 'Subject: ', subject
        print 'Body: \n', prettify_html(html)


def prettify_html(html):
    """ Tries to strip html tags and return just the packed html content

    Used in debugging to print email html content to console without clutter

    """
    try:
        # Try to remove html tags and just print the text content
        texts = bs4.BeautifulSoup(html).findAll(text=visible_text)
        #visible_texts = filter(visible_text, texts)
        cleaned_text = re.sub(
            "\n\n+",
            "\n",
            "".join(
                text.lstrip() if text.lstrip() else text
                for text in texts
            )
        )

    except:
        cleaned_text = html

    return cleaned_text


def visible_text(element):
    return element.parent.name not in \
        ['style', 'script', '[document]', 'head', 'title'] \
        and not isinstance(element, bs4.Comment)
