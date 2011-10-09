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
import time
from urlparse import urljoin
from sc2profile.light_profile import LightProfile


class InvalidUrl(Exception): pass


class Profile(LightProfile):
    """This class provide full profile informations, that means it
    will fetch all profile pages, and it takes some time. Use it only if
    this is what you need. For most common case LightProfile is enought.
    Anyway, all interesting methods are public, so you can call them to
    avoid a full profile dump."""

    achievements = {}
    custom_game = {}
    combat = {}
    exploration = {}
    feats_of_strenght = {}
    matches_history = {}
    quick_match = {}
    recently_earned = {}

    def __init__(self, profile_url):
        """ Initialize Profile class, nothing special just call
        LightProfile constructor in order to update required browser
        and _profile_url"""

        LightProfile.__init__(self, profile_url)

    def _request_to_html(self, url):
        """Fetch an html page and transform it to a xml.html object,
        in order to work with xpath."""

        try:
            response = self._browser.fetch(url)
        except urllib2.URLError:
            raise InvalidUrl('%s is not a valid url' % url)
        content = response.read()
        content = content.decode('utf8').encode('utf8')
        html = lhtml.document_fromstring(content)
        return html

    def update(self):
        """Full profile dump, this method is a wrapper around other public
        methods. It will call all methods, to populate itself with profile
        informations."""

        start_time = time.time()
        self._update_summary()
        self.update_matches_history()
        self.update_recently_earned()
        self.update_achievements()
        self.update_exploration()
        self.update_custom_game()
        self.update_quickmatch()
        self.update_combat()
        self.update_feats_of_strenght()
        self._generation_time = str(round(time.time() - start_time, 3)) + " s"

    def update_matches_history(self):
        """Fetch matches history, and collect all available informations."""

        url = urljoin(self._profile_url, 'matches')
        html = self._request_to_html(url)
        self.matches_history = {i + 1: { #XXX optimise tr.xpath
            'map': tr.xpath("td")[1].text,
            'type': tr.xpath("td")[2].text,
            'date': tr.xpath("td")[4].text.strip(),
            'outcome': tr.xpath("td")[3].xpath("span")[0].text.strip(),
            'speed': tr.xpath("td")[0].xpath("div")[0].text_content().split()[-1]
        } for i, tr in enumerate(
                html.xpath("//table[@class='data-table']/tbody/tr"))}

    def update_achievements(self):
        """Fetch liverty campaign achievements, and collect all available
        informations."""

        self.achievements = {
            'liberty_campaign': {
                'Mar Sara Missions': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211278')),
                'Colonist Missions': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211279')),
                'Covert Missions': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211280')),
                'Rebellion Missions': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211281')),
                'Artifact Missions': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211282')),
                'Prophecy Missions': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211283')),
                'Final Missions': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211284')),
                'Story Mode': self.handle_achievements(
                    urljoin(self._profile_url, 'achievements/category/3211285')),
                }
        }

    def update_exploration(self):
        """Fetch exploration achievements, and collect all available
        informations."""

        self.exploration = {
            'Guide one': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325398')),
            'Guide two': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325399')),
            'Guide three': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325400')),
            'Challanged': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325401')),
        }

    def update_custom_game(self):
        """Fetch custom game achievements, and collect all available
        informations."""

        self.custom_games = {
            'Meduim Ai': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325392')),
            'Hard Ai': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325395')),
            'Very Hard Ai': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325396')),
            'Insane Ai': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325402')),
            'Outmatched': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325397')),
            'Blizzard Mods': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/3211287')),
        }

    def update_quickmatch(self):
        """Fetch quick match achievements, and collect all available
        informations."""

        self.quick_match = {
            'Solo League': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325378')),
            'Team League': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325385')),
            'Competitive': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/4325391')),
        }

    def update_combat(self):
        """Fetch combat achievements, and collect all available
        informations."""

        self.combat = {
            'Economy': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/3211270')),
            'Melee Combat': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/3211271')),
            'League Combat': self.handle_achievements(
                urljoin(self._profile_url, 'achievements/category/3211272')),
        }

    def update_feats_of_strenght(self):
        """Fetch feats of strenght achievements, and collect all available
        informations."""

        self.feats_of_strengh = self.handle_achievements(
            urljoin(self._profile_url, 'achievements/category/4325394')),

    def update_recently_earned(self):
        """Fetch recently earned achievements, and collect all available
        informations."""

        url = urljoin(self._profile_url, 'achievements/')
        html = self._request_to_html(url)
        self.recently_earned = {i: {
            'id': a.get('href').split('/')[-1],
            'date': a.xpath("span")[1].text,
            'title': a.text_content().strip().split('\r')[0]
        } for i, a in enumerate(
            html.xpath("//div[@id='recent-achievements']/a"))}

    def handle_achievements(self, url):
        """As all achievements are similar, we can call a unique method to
        process each page the same way."""

        html = self._request_to_html(url)

        def _date_points_wrapper(el, y):
            """A small cheat around date and points information."""

            return el.xpath("div/div")[0].text_content().strip().split('\r')[y].strip()

        return {el.get('id').split('-')[-1]: {
            'earned': 'unearned' not in el.get('class'),
            'date': _date_points_wrapper(el, -1),
            'points': _date_points_wrapper(el, 0),
            'name': el.xpath("div/div")[2].text_content().strip().split('\r')[0].strip(),
            'description': el.xpath("div/div")[2].text_content().strip().split('\r')[1].strip()
        } for el in html.xpath("//div[@id='achievements-wrapper']/div")}
