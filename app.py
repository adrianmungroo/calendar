import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import math

df = pd.read_csv('calendar.csv')
df['duration'] = (df['end'] - df['start'])*60
df = df.sort_values(['day','start']).reset_index()
df['true_start'] = df['start'] + df['day']*24
df['true_end'] = df['end'] + df['day']*24

events = df.copy()

utc_now = datetime.now(pytz.utc)
atlanta_tz = pytz.timezone('America/New_York')
atlanta_time = utc_now.astimezone(atlanta_tz)
current_time = atlanta_time.time()
current_day = atlanta_time.weekday()
true_time = current_day*24 + current_time.hour + current_time.minute/60 + current_time.second/(60*60)

def get_current_task(events=events, true_time=true_time):
    time_mask = (events['true_start'] <= true_time) & (events['true_end'] > true_time)
    try:
        current_event = events[time_mask]
        current_event_title = events[time_mask]['title'].values[0]
        duration = (current_event['true_end'] - true_time).values[0]
    except:
        current_event_title = 'Nothing'
        duration = ''
    return current_event_title, duration
    
def get_next_task(events = events, true_time = true_time):
    try:
        next_task = events[events['true_start'] > true_time].iloc[0]
        time_until = next_task['true_start'] - true_time
        next_task_title = next_task['title']
    except: # no more tasks for the week, the list has ended
        next_task = events.iloc[0]
        next_task_title = next_task['title']
        time_until = next_task['true_start'] + (7 + next_task['day'])*24 - true_time
    finally:
        return next_task_title, time_until

current_task, duration = get_current_task()
next_task, time_until = get_next_task()

if duration:
    duration_hours = math.floor(duration)
    duration_minutes = math.floor((duration - duration_hours)*60)
    duration_seconds = math.floor(((duration - duration_hours)*60 - duration_minutes)*60)

until_next_hours = math.floor(time_until)
until_next_minutes = math.floor((time_until - until_next_hours)*60)
until_next_seconds = math.floor(((time_until - until_next_hours)*60 - until_next_minutes)*60)

st.markdown(
    """
    <style>
    .current-task {
        font-size: 48px;  /* Large font size for current task */
        color: #ff6347;   /* Tomato color for prominence */
        font-weight: bold; /* Bold font for emphasis */
        margin-bottom: 30px; /* Space below current task */
    }
    .other-task {
        font-size: 24px;  /* Smaller font size for other tasks */
        color: #555;      /* Grey color for less emphasis */
        margin-bottom: 5px; /* Space below other tasks */
    }
    .exception {
        font-size: 15px;  /* Smaller font size for other tasks */
        color: #555;      /* Grey color for less emphasis */
        margin-bottom: 5px; /* Space below other tasks */
    }
    .refresh-button {
        margin-top: 10px; /* Space above the button */
    }
    </style>
    """,
    unsafe_allow_html=True
)

if duration:
    st.markdown(f'<div class="current-task">DO {current_task}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="other-task">FOR {duration_hours} hours, {duration_minutes} minutes, and {duration_seconds} seconds</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="other-task">NEXT {next_task}</div>', unsafe_allow_html=True)
    if duration != time_until: # if there is a gap of nothing after the current task and the next one
        st.markdown(f'<div class="exception">IN {until_next_hours} hours, {until_next_minutes} minutes, and {until_next_seconds} seconds </div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="current-task">DO {current_task}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="other-task">UNTIL {next_task} \n\n IN {until_next_hours} hours, {until_next_minutes} minutes, and {until_next_seconds} seconds</div>', unsafe_allow_html=True)

st.button("Refresh")