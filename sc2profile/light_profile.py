#!/usr/bin/env python
"""
----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <srounet@gmail.com> wrote this file. As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return Fabien Reboia
 * ----------------------------------------------------------------------------
"""


import lxml.html as lhtml
import re
import time
import urllib2
import sc2profile
from sc2profile import browser


class InvalidProfileUrl(Exception): pass


class LightProfile(object):
    """This class is a wrapper that collect all available data on a
    starcraft2 bnet landing page with only one http request.
    The aim of this class is to provide a low cost method to grab a small set
    of informations on a given profile."""

    _generation_time = None

    achievement_points = None
    campaign = None
    game_played = {}
    league_win = None
    most_played_race = None
    name = None
    season_snapshot = {}
    top_achievements = {}
    portrait = {}

    def __init__(self, profile_url):
        """Initialize a new profile object, with profile_url as
        current profile.

        profile_url must match a valid bnet url.
        example: http://eu.battle.net/sc2/en/profile/1041236/1/nopz/"""

        self._profile_url = profile_url
        if sc2profile.proxy_url:
            proxy_browser = browser.HTTPProxyBrowser(sc2profile.proxy_url)
            browser.install_browser(proxy_browser)
        self._browser = sc2profile.browser.default_browser

    def update(self):
        """Update current profile, with landing page informations."""

        start_time = time.time()
        self._update_summary()
        self._generation_time = str(round(time.time() - start_time, 3)) + " s"

    def _update_summary(self):
        """Fetch profile landing page in order to collect standard
        informations.

        Use default_browser in order to download in memory landing page, and
        transforms to a xpath ready object with lxml.
        With xpath facilities updates profile, and sets different informations
        available for usage.
        """

        try:
            response = self._browser.fetch(self._profile_url)
        except urllib2.URLError:
            raise InvalidProfileUrl('%s is not a valid profile url' %
                                    self._profile_url)
        profile_content = response.read()
        profile_content = profile_content.decode('utf8')
        html = lhtml.document_fromstring(profile_content)

        percentage_wrapper = lambda x: round(float(x.split(' ')[1][:-1]), 2)
        game_wrapper = lambda el, y: el.xpath("div[contains(@class, 'bars')]/"
            "div/div/span/text()")[y]
        div_wrapper = lambda el, y: el.xpath("div[contains(@class, 'ladder')]/"
            "div/div[2]/text()")[y]
        link_wrapper = lambda el: ("http://eu.battle.net%s" %
                                  el.xpath("div[contains(@class, 'ladder')]/"
                                      "a")[0].get('href'))

        self.name = xpath_value(html.xpath("//div[@id='profile-header']/h2/a/text()"))
        self.achievement_points = xpath_value(html.xpath("//div[@id='profile-header']/"
            "h3/text()"))
        self.most_played_race = xpath_value(html.xpath("//div[@id='season-snapshot']/"
            "div[@class='module-footer']/a/@class"))
        if self.most_played_race:
            self.most_played_race = self.most_played_race.replace('race-', '')
        self.league_win = xpath_value(html.xpath("//div[@id='career-stats']/"
            "div[contains(@class, 'module-body')]/h2/text()"))
        self.campaign = xpath_value(html.xpath("//div[@id='career-stats']/"
            "div[contains(@class, 'module-body')]/h4[3]/text()"))

        self.game_played = {list(el.itertext())[2].strip():
             int(el.xpath('span/text()')[0]) for
                 el in html.xpath("//div[@id='career-stats']/"
                    "div[contains(@class, 'module-body')]/ul/li")}

        self.top_achievements = {
            el.xpath("a/text()")[1].strip() : {
                'points' : int(el.xpath("div/span/text()")[0]),
                'percentage':  percentage_wrapper(
                    el.xpath("div/div/div")[0].get('style')
                )
            } for el in html.xpath("//div[@id='top-achievements']/div")}

        def _games_wrapper(el, y):
            """On some profile, the win ratio is not available.
            This wrapper is here to profide a unique interface
            for win/games informations."""

            bars_el = el.xpath("div[contains(@class, 'bars')]/div")
            if len(bars_el) == 1: # Game ratio (games/win) not available
                if y == 1: return None
                return float(bars_el[0].xpath("div/span/text()")[0].split()[0].replace(',', '.'))
            return float(bars_el[y].xpath("div/span/text()")[0].split()[0].replace(',', '.'))

        self.season_snapshot = {
            el.xpath("div[contains(@class, 'division')]")[0].text: {
                'games': _games_wrapper(el, 0),
                'win': _games_wrapper(el, 1),
                'name': div_wrapper(el, 1),
                'rank': int(div_wrapper(el, 2).strip()),
                'link': link_wrapper(el)
            } for el in html.xpath("//div[@id='season-snapshot']/"
                "div[contains(@class, 'module-body')]/div")
            if 'empty-season' not in el.get('class')}

        portrait_span = html.xpath("//span[contains(@class, 'icon-frame')]/@style")[0]
        pict_reg = r""".*portraits/([0-9\-]+).jpg.* ([\w\-]+) ([\w\-]+) """
        match = re.search(pict_reg, portrait_span, re.DOTALL)
        if match:
            self.portrait['pict'] = match.groups()[0]
            self.portrait['width'] = match.groups()[1]
            self.portrait['height'] = match.groups()[2]

def xpath_value(xpath_node, default=None):
    if not xpath_node:
        return default
    return xpath_node[0]
