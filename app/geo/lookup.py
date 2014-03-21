# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import urllib2

from app import app


GEO_IP_SERVICE = "http://freegeoip.net/json/{ip}"


def iplookup(ip):
    """ Returns a dictionary of geo data for a given ip address

    Returns an empty dictionary if no data is found
    """
    ip = (ip or '').strip()

    if not ip:
        return {}

    url = GEO_IP_SERVICE.format(ip=ip)

    try:
        geo_data = urllib2.urlopen(url).read()
    except urllib2.HTTPError as e:
        app.logger.error(
            "Error loading geo data from service: {url}\n"
            "{error}".format(url=url, error=e))
        return {}

    try:
        return json.loads(geo_data)
    except ValueError as e:
        app.logger.error(
            "Error parsing json geo data for ip: {ip}\n"
            "{error}".format(ip=ip, error=e))
        return {}
