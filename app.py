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
        current_event = events[time_mask]['title'].values[0]
    except:
        current_event = 'Nothing'
    return current_event
    
def get_next_task(events = events, true_time = true_time):
    next_task = events[events['true_start'] > true_time].iloc[0]
    time_until = next_task['true_start'] - true_time
    next_task_title = next_task['title']
    return next_task_title, time_until

current_task = get_current_task()
next_task, time_until = get_next_task()

hours_until = math.floor(time_until)
minutes_until = math.floor((time_until - hours_until)*60)
seconds_until = math.floor(((time_until - hours_until)*60 - minutes_until)*60)

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
        margin-bottom: 15px; /* Space below other tasks */
    }
    .refresh-button {
        margin-top: 10px; /* Space above the button */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display tasks with styling
st.markdown(f'<div class="current-task">DO {current_task}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="other-task">FOR {hours_until} hours, {minutes_until} minutes, and {seconds_until} seconds</div>', unsafe_allow_html=True)
st.markdown(f'<div class="other-task">UNTIL {next_task}</div>', unsafe_allow_html=True)
st.button("Refresh")