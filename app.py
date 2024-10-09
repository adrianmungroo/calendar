import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

df = pd.read_csv('calendar.csv')
df['duration'] = (df['end'] - df['start'])*60
df = df.sort_values(['day','start']).reset_index()
events = df.copy()

utc_now = datetime.now(pytz.utc)
atlanta_tz = pytz.timezone('America/New_York')
atlanta_time = utc_now.astimezone(atlanta_tz)
current_time = atlanta_time.time()
current_day = atlanta_time.weekday()
current_hour_fraction = current_time.hour + current_time.minute/60 + current_time.second/(60*60)

def get_current_task(events = events, current_day = current_day, current_hour_fraction = current_hour_fraction):
    try:
        day_mask = events['day'] == current_day
        time_mask = (events['start'] <= current_hour_fraction) & (events['end'] > current_hour_fraction)
        current_event = events[day_mask & time_mask]
        current_event_title = current_event['title'].values[0]
        current_event_index = current_event.index[0]

        event_string = f'#### Right now, you should be doing ... \n # :rainbow[{current_event_title}]'
        return event_string, current_event_index
    except: #obtained no event, get last one. NO NEED TO GET THE ONE RIGHT BEFORE THE CURRENT TIME
        time_mask = (events['start'] <= current_hour_fraction)
        last_event_index = events[day_mask and time_mask].index[-1]
        return f'# :rainbow[You have nothing to do right now]', last_event_index
    
def get_next(index, events = events, current_hour_fraction = current_hour_fraction):
    try:
        current_day = events.iloc[index]['day']
        next_day = events.iloc[index + 1]['day']
        next = events.iloc[index + 1]
        next_title = next['title']
        if next_day == current_day:
            time_left = (next['start'] - current_hour_fraction)*60
        else:
            time_left = (24*(next_day - current_day) + next['start'] - current_hour_fraction)*60
        return next_title, time_left
    except: # end of the week rollover
        next = events.iloc[0]
        next_title = next['title']
        time_left = (24*(7 - current_day) + next['start'] - current_hour_fraction)*60
        return next_title, time_left

current_event_string, current_event_index = get_current_task()
next_title, time_left = get_next(current_event_index)

st.write(f"{current_event_string}")
st.write(f"{next_title} in... \n\n :rainbow[{round(time_left,2)} minutes]")
