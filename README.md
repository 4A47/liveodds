<p align="center">
  <img src="https://i.postimg.cc/g2z1WmkG/liveodds-tp.png">
</p>

<p align="center">
  <img src="https://i.postimg.cc/6pC44nV9/build-joints-brightgreen.png">
  <img src="https://i.postimg.cc/DmkBxCk0/joint-passing-brightgreen.png">
  <img src="https://i.postimg.cc/3NDtjsqz/checks-bouncing-brightgreen.png">
  <img src="https://i.postimg.cc/0Q4twkVp/comments-0-yellowgreen.png">
</p>

Python API for Horse Racing odds

<br>

#### Table of Contents
- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [API](#api)
    - [Meeting](#meeting)
    - [Race](#race)
    - [Examples](#examples)
- [Disclaimer](#disclaimer)

<br>

## Requirements
Python 3.7 or greater is needed, you can get the latest version [here](https://www.python.org/downloads/). In addition, the modules [lxml](https://lxml.de/), [requests](https://requests.readthedocs.io/en/master/), [aiohttp](https://docs.aiohttp.org/en/stable/) are needed. They can be installed using PIP(included with Python) with the following command.

` pip3 install lxml requests aiohttp`

<br>

## Install

Clone the repo with [git](https://git-scm.com/downloads)

`git clone https://github.com/4A47/liveodds.git`

or [download](https://github.com/4A47/liveodds/archive/main.zip) the zip.


<br>

## Usage

Copy the **inner** liveodds folder to your project and import with the following line:

```python
from liveodds.racing import Racing
```

<br>


## API

There are 3 classes, **Racing**, **Meeting** and **Race**. The Racing class provides a few methods to assist in accessing Meeting objects which contain Race objects for each race at the meeting.

<details>
<summary>Racing class details</summary>

#### Racing Class: Methods and Properties

| Methods                                      | Description                                                                          |
|----------------------------------------------|--------------------------------------------------------------------------------------|
| courses(date: str, region: str)              | Returns a list of string course names for a given date and region                    |
| dates()                                      | Returns a list of string dates where races are available                             |
| meeting(date: str, region: str, course: str) | Returns a specific meeting object for a given date, region and course                |
| meetings(date: str, region: str)             | Returns a list of Meeting objects for all meetings on a given date in a given region |
| meetings_dict(date: str, region: str)        | Returns a dict of Meeting objects for all meetings on a given date in a given region |
| meetings_json(date: str, region: str)        | Returns a JSON string with odds for all meetings on a given date in a given region   |
| regions(date: str)                           | Returns a list of string region codes for a given date                               |


</details>

<br>

### Meeting

**Meeting objects** contain information about a meeting, methods to get all odds for a meeting in dictionary or JSON format, and Race objects for each race at the meeting. Meeting objects are stored in a nested dictionary in the Racing class and can be accessed using the convenience methods provided, or directly from the underlying Racing._meetings dictionary for the criminally insane.

Meeting objects can be retrieved using the following methods in the Racing class:

#### Racing.meeting(date: str, region: str, course: str)
_Returns a specific meeting object_


#### Racing.meetings(date: str, region: str)
_Returns a list of meeting objects for a given date and region._

<br>

<details>
<summary>Meeting Class details</summary>

#### Meeting class: Methods and Properties

| Methods          | Description                                                      |
|------------------|------------------------------------------------------------------|
| json()           | Returns a JSON string of odds for all races at meeting           |
| odds()           | Returns a dict of odds for all races at meeting                  |
| race(time: str)  | Returns a specific Race object from meeting for a given off time |
| races()          | Returns a list of Race objects for all races at meeting          |
| races_dict()     | Returns a dict of Race objects for all races at meeting          |
| times()          | Returns a list of string off times for all races at meeting      |


| Properties       | Description                               |
|------------------|-------------------------------------------|
| date: str        | Date of the meeting                       |
| region: str      | 2 or 3 letter region code (ALL CAPS)      |
| course: str      | Name of the course                        |

</details>

<br>

### Race

**Race objects** contain information and odds for a race, they are retrieved using the following methods in the Meeting class:

#### Meeting.race(time: str)
_Returns a specific race object given a start time ie '14:30'_


#### Meeting.races()
Returns a list of race objects for all races in the meeting.

<br>
<details>
<summary>Race class details</summary>

#### Race class: Methods and Properties

| Methods                 | Description                                                                       |
|-------------------------|-----------------------------------------------------------------------------------|
| json()                  | Returns JSON string of odds for every horses in race                              |
| horses()                | Returns a list of string: horses in the race                                      |
| odds(horse: str = None) | Returns odds dictionary for specific horse if given, otherwise all horses in race |
| update_odds()           | Updates the odds of the race                                                      |


| Properties      | Description                                             |
|-----------------|---------------------------------------------------------|
| course :str     | The name of the course                                  |
| date: str       | Date of the race                                        |
| region: str     | 2 or 3 letter region code (ALL CAPS)                    |
| time :str       | The off time of the race                                |
| title: str      | The name of the race (Very inconsistent outside UK/IRE) |

</details>
<br>


### Examples

You can target meetings and races specifically as will be shown, or you can simply get a JSON string for every meeting for a date and region:

```python
from liveodds.racing import Racing

racing = Racing()

today = racing.dates()[0]

json = racing.meetings_json(today, 'UK')

print(json)
```

the JSON viewer shows an example output

![meetingsJSON](https://i.postimg.cc/HWfNg1GZ/meetings.png)

<br>


If you only care about some races or meetings, you can get them more efficiently using the Meeting and Race objects. Methods to retrieve meeting objects generally take as parameters a date, and a region code, which is an all caps 2 or 3 letter code, i.e 'UK' or 'IRE'. 

In the following example we get Meeting objects for a random region and access the odds dictionary for each meeting:

```python
from liveodds.racing import Racing

racing = Racing()

today = racing.dates()[0]

region = racing.regions(today)[0]

for meeting in racing.meetings(today, region):
    odds = meeting.odds()
    print(meeting.course, odds)
```

<br>

The json method works exactly the same as odds() but returns a JSON string as opposed to a dictionary. In the following example we target a specific meeting by providing the date, region and course name.

```python
from liveodds.racing import Racing

racing = Racing()

today = racing.dates()[0]
region = racing.regions(today)[0]
course = racing.courses(today, region)[0]

meeting = racing.meeting(today, region, course)

print(meeting.json())
```

The JSON viewer shows the structure clearly:

![json](https://i.postimg.cc/T38JDQM4/odds.png)


<br>


The Race.odds() method returns a dictionary where the key is the name of the horse, and the value is a dictionary of bookies odds. You can optionally pass a specific horse, and a keyword bookie to filter the return. If only the bookie is given it returns odds for all horses with the given bookie. 

In the following example we get a random race and horse in the UK, and watch its odds with a random bookie. The is just to show how to target specific horses and bookies if required.

```python
from liveodds.racing import Racing
from time import sleep, strftime


def watch_horse(race, horse, bookie):
    while True:
        race.update_odds()
        odds = race.odds(horse, bookie=bookie)
        print(f'{race.course} {race.time} - {horse}: {odds} ({bookie}) @ {strftime("%H:%M:%S")}')
        sleep(3)


racing = Racing()

today = racing.dates()[0]
courses = racing.courses(today, 'UK')
meeting = racing.meeting(today, 'UK', courses[0])
race = meeting.race(meeting.times()[0])

horse = race.horses()[0]
bookie = race.bookies()[0]

watch_horse(race, horse, bookie)
```
<br>

You can return a JSON string instead of a dictionary with the Race.json() method. A view of the json should make the structure clear.

![json](https://i.postimg.cc/kgxLHfx0/race.png)

<br>

#### Disclaimer
I hereby renounce all liability when the MI6 cybercrime net inevitably closes in on users of this API. If you do, in a moment of misguided recklessness, decide to use this API, you *will* go to jail, no ifs, buts or maybes, the cost of doing business here is hard time. So before you clone, ask yourself just how much you really want access to the latest odds in a python script, and is it worth throwing your life away for it? Would you torrent a car?
