#!/usr/bin/env python3
import sys

sys.path.append('../')

from liveodds.racing import Racing

"""
There are only 2 objects to care about - Meeting and Race

Meeting objects are stored in a nested dict in the Racing class.
Race objects are then retrieved from methods in Meeting class.

The underlying dict Racing._meetings can be accessed directly 
the structure is as follows:

        date: str
            region: str
                meeting: str
    
        meeting = racing._meetings[date][region][course]
    
    Example:
    
        meeting = racing._meetings['2021-03-05']['UK']['Newbury']
    

Or using some convenience functions

        meetings = racing.meetings(date, region)
            
        meeting = racing.meeting(date, region, course)
        
    Example:
    
        meetings = racing.meetings('2021-03-05', 'UK')
        
        meeting = racing.meeting('2021-03-05', 'UK', 'Newbury')

"""

racing = Racing()

# get list of dates which have races available
# ordered so 0 index guaranteed to be today's date
dates = racing.dates()
today = dates[0]

print(f'\nAvailable dates: {dates}\n\nTodays date: {today}\n')


# get list of regions for a given date
regions = racing.regions(today)

print(f'Regions on {today}: {regions}\n')


# get list of courses for a given date and region
courses = racing.courses(today, regions[0])

print(f'Courses in {regions[0]}: {courses}\n')


# get list of meeting objects for a given date and region
meetings = racing.meetings(today, regions[0])

print(f'Meeting objects for {today} in {regions[0]}: {meetings}\n')


# get a specific meeting
meeting = racing.meeting(today, regions[0], courses[0])

print(f'Meeting object for {courses[0]}: {meeting}\n')
print(f'Meeting date: {meeting.date}')
print(f'Meeting region: {meeting.region}')
print(f'Meeting course: {meeting.course}\n')


# get race objects for a meeting
races = meeting.races()

print(f'Race objects for {courses[0]}: {races}\n')


# get list of times for races in a meeting
times = meeting.times()

print(f'Race starting times for {meeting.course}: {times}\n')


# get object for a specific race
race = meeting.race(times[0])

print(f'Race object for {times[0]} {meeting.course}: {race}\n')


# get list of horses in a race
horses = race.horses()

print(f'Horses in {race.time} {race.course}: {horses}\n')


# get a dict of odds for the full race
race_odds = race.odds()

print(f'Odds for {race.time} {race.course}:\n')

for horse in race_odds:
    print(f'{horse}: {race_odds[horse]}')


# get dict of odds for specific horse
horse_odds = race.odds(horses[0])

print(f'\nOdds for {horses[0]}: {horse_odds}')


# update latest odds for a race object
race.update_odds()
