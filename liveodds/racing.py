from .utils.utils import *

from collections import defaultdict
from json import dumps
from requests import Session


class Racing:

    def __init__(self):
        self._meetings = defaultdict(lambda: defaultdict(dict))
        self.session = Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})
        self._get_meetings()

    def _get_meetings(self):
        doc = document('https://www.oddschecker.com/horse-racing', self.session)

        for section in tags_with_attrib(doc, '//div', 'data-day'):
            date = get_date(section.attrib['data-day'])

            for meeting in tags_with_class(section, '//div', 'race-details'):
                course = meeting.find('.//a').text
                region = meeting.find('.//span/span').text
                races = tag_with_class(meeting, '//div', 'all-todays-races')
                race_links = races.findall('.//a')
                self._meetings[date][region][course] = Meeting(date, course, region, race_links, self.session)

    def courses(self, date, region):
        return [course for course in self._meetings[date][region]]

    def dates(self):
        return sorted([*self._meetings.keys()])

    def meeting(self, date, region, course):
        return self._meetings[date][region][course]

    def meetings(self, date, region):
        return [self._meetings[date][region][course] for course in self._meetings[date][region]]

    def meetings_dict(self, date, region):
        return self._meetings[date][region]

    def regions(self, date):
        return [region for region in self._meetings[date]]


class Meeting:

    def __init__(self, date, course, region, race_links, session):
        self.course = course
        self.date = date
        self.region = region
        self._races = {}
        self.session = session
        self.init_races(race_links)

    def __repr__(self):
        return f'Meeting({self.course} ({self.region}), {self.date})'

    def __dir__(self):
        return self.__dict__.keys()

    def init_races(self, race_links):
        for race in race_links:
            time = race.text_content()
            title = race.attrib['title']
            url = race.attrib['href']
            self._races[time] = Race(self.course, self.date, self.region, time, title, url, self.session)

    def json(self):
        json = {}
        for race in self.races():
            json[race.time] = race.odds()

        return dumps(json)

    def odds(self):
        odds = {}
        for race in self.races():
            odds[race.time] = race.odds()

        return odds

    def parse_docs(self, docs):
        for doc in docs:
            _url = tag_with_attrib(doc, '//meta', 'property="og:url"')
            key = _url.attrib['content'].split('/')[5]
            try:
                self._races[key].parse_odds(doc.find('.//tbody'))
            except KeyError:
                off_time = tag_with_classes(doc, '//a', ('race-time', 'active'))
                self._races[off_time.text].parse_odds(doc.find('.//tbody'))

    def race(self, key):
        doc = document(self._races[key].url, self.session)
        self._races[key].parse_odds(doc.find('.//tbody'))

        return self._races[key]

    def races(self):
        urls = [self._races[key].url for key in self._races]

        docs = asyncio.run(documents_async(urls))
        self.parse_docs(docs)

        return [self._races[race] for race in self._races]

    def races_dict(self):
        urls = [self._races[key].url for key in self._races]

        docs = asyncio.run(documents_async(urls))
        self.parse_docs(docs)

        return self._races

    def times(self):
        return list(sorted(self._races.keys()))


class Race:

    def __init__(self, course, date, region, time, title, url, session):
        self._bookies = racing_bookies()
        self._odds = {}
        self.course = course
        self.course = course
        self.date = date
        self.region = region
        self.session = session
        self.time = time
        self.title = title
        self.url = 'https://www.oddschecker.com' + url

    def __dir__(self):
        return self.__dict__.keys()

    def __repr__(self):
        return f'Race({self.course} {self.time}, {self.date})'

    def bookies(self):
        return [bookie for bookie in self._bookies.values()]

    def horses(self):
        return [horse for horse in self._odds.keys()]

    def json(self):
        return dumps(self._odds)

    def odds(self, horse=None):
        if horse:
            return self._odds[horse]
        else:
            return self._odds

    def parse_odds(self, odds_table):
        for row in odds_table.findall('./tr'):
            horse = row.attrib['data-bname']
            # num = tag_with_class(row, '/td', 'cardnum').text
            odds = {}

            for book in self._bookies:
                price = tag_with_attrib(row, '/td', f'data-bk="{book}"').attrib['data-odig']
                odds[self._bookies[book]] = price

            self._odds[horse] = odds

    def update_odds(self):
        doc = document(self.url, self.session)
        self.parse_odds(doc.find('.//tbody'))
