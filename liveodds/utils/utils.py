import aiohttp
import asyncio
from datetime import datetime, timedelta
from lxml import html
import requests


_racing_bookies = {
    "B3": "bet365",
    "SK": "Sky Bet",
    "PP": "Paddy Power",
    "WH": "William Hill",
    "EE": "888sport",
    "FB": "Betfair Sportsbook",
    "VC": "Bet Victor",
    "UN": "Unibet",
    "MI": "Mansion Bet",
    "FR": "Betfred",
    "WA": "Betway",
    "BY": "Boylesports",
    "OE": "10Bet",
    "SA": "Sport Nation",
    "VT": "Vbet",
    "RZ": "RedZone",
    "RK": "Smarkets Sportsbook"
}


def get_date(day):
    today = datetime.today()
    date_list = [today + timedelta(days=x) for x in range(6)]
    days = {'today': today.strftime('%Y-%m-%d')}

    for date in date_list[1:]:
        days[date.strftime('%A')] = date.strftime('%Y-%m-%d')

    return days[day]


def racing_bookies():
    return _racing_bookies


def document(url, session):
    r = session.get(url)
    return html.fromstring(r.content)


def tag_with_attrib(element, tag, target):
    return element.find(f'.{tag}[@{target}]')


def tags_with_attrib(element, tag, target):
    return element.xpath(f'.{tag}[@{target}]')


def tag_with_class(element, tag, target):
    return element.find(f'.{tag}[@class="{target}"]')


def tag_with_classes(element, tag, targets):
    target_classes = [f'contains(@class, "{target}")' for target in targets]
    return element.xpath(f'.{tag}[{" and ".join(target_classes)}]')[0]


def tags_with_class(element, tag, target):
    return element.xpath(f'.{tag}[@class="{target}"]')


async def documents_async(urls):
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector())
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    ret = await asyncio.gather(*[get_document(url, session) for url in urls])
    await session.close()
    return ret


async def get_document(url, session):
    async with session.get(url) as response:
        resp = await response.text()
        return html.fromstring(resp)
