import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

events = pd.read_csv('calendar.csv')

def get_current_task(events):
    utc_now = datetime.now(pytz.utc)
    atlanta_tz = pytz.timezone('America/New_York')
    atlanta_time = utc_now.astimezone(atlanta_tz)
    current_time = atlanta_time.time()
    current_day = atlanta_time.weekday()
    current_hour_fraction = current_time.hour + current_time.minute/60
    
    day_mask = events['day'] == current_day
    time_mask = (events['start'] <= current_hour_fraction) & (events['end'] >= current_hour_fraction)

    color = 'rainbow'

    event_string = f'#### Right now, you should be doing ... \n # :{color}[{events[day_mask & time_mask]["title"].values[0].upper()}]'
    return event_string

st.write(f"{get_current_task(events)}")
