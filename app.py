import streamlit as st
import pandas as pd
from datetime import datetime

events = pd.read_csv('calendar.csv')

def get_current_task(events):
    current_time = datetime.now().time()
    current_day = datetime.now().weekday()
    current_hour_fraction = current_time.hour + current_time.minute/60
    
    day_mask = events['day'] == current_day
    time_mask = (events['start'] <= current_hour_fraction) & (events['end'] >= current_hour_fraction)

    color = 'rainbow'

    event_string = f'#### Right now, you should be doing ... \n # :{color}[{events[day_mask & time_mask]["title"].values[0].upper()}]'
    return event_string

st.write(f"{get_current_task(events)}")