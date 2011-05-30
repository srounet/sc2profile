#!/usr/bin/env python
"""
----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <srounet@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Fabien Reboia
 * ----------------------------------------------------------------------------
"""

import urllib2


class Browser(object):
    """A wrapper around http web requests."""

    def __init__(self):
        """Nothing special, we just need the standard urlib2
        opener here."""

        self.opener = self._build_opener()

    def fetch(self, url, headers=None):
        """Make an http request and return the response.
        Will raise and urllib2.URLError if something bad happend."""

        request = self._build_request(url, headers=headers)
        try:
            response = self.opener.open(request)
        except urllib2.URLError as err:
            err.opener = self.opener
            err.request = request
            raise
        return response

    def _build_opener(self):
        """Create a standard opener for classic web requests."""

        opener = urllib2.build_opener()
        return opener

    def _build_request(self, url, headers=None):
        """Create an urllib2 Request with headers informations if set."""

        request = urllib2.Request(url, None, headers or {})
        return request


class HTTPProxyBrowser(Browser):
    """Inheritate from Browser class, it wrap the classic build opener,
    and add a ProxyHandler, for proxy request usage."""

    def __init__(self, proxy_url):
        """Here we have overrided our opener so we want to call this one
        instead of the classic one. It will add a proxy handler to our
        requests."""

        self.opener = self._build_opener(proxy_url)

    def _build_opener(self, proxy_url):
        """ProxyHandler, add a ProxyHandler to opener."""
        opener = Browser._build_opener(self)
        proxy_handler = urllib2.ProxyHandler({'http': proxy_url})
        opener.add_handler(proxy_handler)
        return opener


default_browser = Browser()


def install_browser(browser):
    """For an easy usage, we use a global default_browser in order to
    provide a unique Browser object for all of our requests."""
    global default_browser
    if not isinstance(browser, Browser):
        raise InvalidBrowserError('invalid browser:', browser)
    default_browser = browser


class InvalidBrowserError(Exception):
    pass
