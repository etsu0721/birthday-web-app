from random import betavariate
from threading import main_thread
import streamlit as st
import datetime as dt
import pytz
from collections import Counter, OrderedDict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup

TZ = pytz.timezone('EST5EDT')
wkday_word_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def count_bdays_by_wkday(today, birthday):
    # Check if it is the user's birthday
    if (today.month == birthday.month) & (today.day == birthday.day):
        st.balloons()

    mo = birthday.month
    d = birthday.day

    # If input birthday has not yet occurred this year, do not count it
    if today < dt.datetime(today.year, mo, d).date():
        birthdays = [dt.datetime(yr, mo, d).date().weekday() for yr in range(birthday.year+1, today.year)]
    # Otherwise, count it
    else:
        birthdays = [dt.datetime(yr, mo, d).date().weekday() for yr in range(birthday.year+1, today.year+1)]
    wkday_counts = (Counter(birthdays))
    
    # Sort Counter object by weekday index for sorted bar plot labels
    wkday_counts = OrderedDict(sorted(wkday_counts.items()))

    # Map Counter object keys (integers representing weekdays) to weekday words: wkday_counts
    wkday_counts = np.array([*map(lambda k: (wkday_word_map[k], wkday_counts[k]), wkday_counts.keys())])

    return wkday_counts

def plot_wkday_counts_bar_plt(wkday_counts):
    if len(wkday_counts) == 0:
        return
    else:
        x_coord = np.arange(len(wkday_counts))
        heights = wkday_counts[:, 1].astype(int)
        labels = wkday_counts[:, 0]
        fig, ax = plt.subplots()
        ax.bar(x_coord, heights, tick_label=labels)
        plt.title('Number of birthdays by day of week')
        plt.ylabel('Frequency')
        y_range = [*range(heights.max()+1)]
        plt.yticks(ticks=y_range)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    return

def write_age(today, birthday):
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    age_str = 'You are **{}** years old.'.format(age)
    st.write(age_str)
    return

def write_wkday_born(birthday):
    wkday_str = 'You were born on a **{}**.'.format(wkday_word_map[birthday.weekday()])
    st.write(wkday_str)
    return

def write_moon_phase(yr, mo, day):
    url = 'https://www.moongiant.com/phase/{}'.format('/'.join((mo, day, yr)))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    phase_details = soup.find(name='div', attrs={'id':'moonDetails'})
    moon_phase = phase_details.find_next(name='span').text
    illumination = phase_details.find_next(name='span').find_next(name='span').text
    moon_phase_str = 'On your birthdate, \
        the moon was in the **{}** phase at **{}** illumination. ([source]({}))'.format(moon_phase, illumination, url)
    st.write(moon_phase_str)
    return

def write_birthday_facts(today, birthday):
    st.write('## Birthday facts')
    write_age(today, birthday)
    write_wkday_born(birthday)
    write_moon_phase(str(birthday.year), str(birthday.month), str(birthday.day))
    return

def setup_webpage():
    st.set_page_config(layout="wide")
    st.title('Birthday Web App')
    return

def get_user_birthdate():
    min_date = dt.datetime(1900, 1, 1)
    max_date = dt.datetime.now(TZ)
    birthday = st.date_input('Select your birthday', min_value=min_date, max_value=max_date)
    return birthday

def main():
    setup_webpage()
    birthday = get_user_birthdate()

    if st.button('Calculate'):     # Upon user to clicking button
        today = dt.datetime.now(TZ).date()
        col1, col2 = st.beta_columns(2)  # Create two columns
        wkday_counts = count_bdays_by_wkday(today, birthday)
        with col1:
            plot_wkday_counts_bar_plt(wkday_counts)
        with col2:
            write_birthday_facts(today, birthday)
    
    return

if __name__ == "__main__":
    main()


#TODO: Celebrities with the same b-day as a Birthday Fact
#TODO: Let user select timeframe (days) and have a dynamic table showing celebrities born within that timeframe
#TODO: Species extention as a b-day fact
#TODO: Most popular car, candy, etc. during birth year as b-day fact
#TODO: Let user pick their favorite sport and return the team who won the championship in their birth year