import streamlit as st
import datetime as dt
import pytz
from collections import Counter, OrderedDict
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

wkday_word_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def calc_wkday_counts(today, b_day):
    # Check if today is user's birthday. If so, wish a happy birthday
    if (today.month == b_day.month) & (today.day == b_day.day):
        st.balloons()

    # Calculate birthdays by day of the week
    mo = b_day.month
    d = b_day.day

    # If input birthday has not yet occurred this year, do not count it
    if today < dt.datetime(today.year, mo, d).date():
        b_days = [dt.datetime(yr, mo, d).date().weekday() for yr in range(b_day.year+1, today.year)]
    # Otherwise, count it
    else:
        b_days = [dt.datetime(yr, mo, d).date().weekday() for yr in range(b_day.year+1, today.year+1)]
    wkday_counts = (Counter(b_days))
    
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

def write_age(today, b_day):
    age = today.year - b_day.year - ((today.month, today.day) < (b_day.month, b_day.day))
    age_str = 'You are {} years old.'.format(age)
    st.write(age_str)
    return

def write_wkday_born(b_day):
    wkday_str = 'You were born on a {}.'.format(wkday_word_map[b_day.weekday()])
    st.write(wkday_str)
    return

def write_birthday_facts(today, b_day):
    st.write('## Birthday facts')
    write_age(today, b_day)
    write_wkday_born(b_day)
    return

def main():
    # Use wide mode for app
    st.set_page_config(layout="wide")

    # Display web app title
    st.title('Birthday Web App')

    # Get user's birthdate
    tz = pytz.timezone('UTC')   
    max_date = tz.localize(dt.datetime.today()) # Ensure max date is based on user's timezone
    min_date = dt.datetime(1900, 1, 1)
    b_day = st.date_input('Select your birthday', min_value=min_date, max_value=max_date)
    b_day = tz.localize(dt.datetime.combine(b_day, dt.datetime.min.time()))

    # Wait for user to click button to proceed
    if st.button('Calculate'):
        today = dt.datetime.utcnow().date()

        # Create two columns
        col1, col2 = st.beta_columns(2)

        # Calculate birthdays by weekday
        wkday_counts = calc_wkday_counts(today, b_day)

        # Plot wkday_counts as bar plot
        with col1:
            plot_wkday_counts_bar_plt(wkday_counts)

        # Write birthday and age facts
        with col2:
            write_birthday_facts(today, b_day)
        
    return

if __name__ == "__main__":
    main()

#TODO: Include moon phase as a Birthday Fact (https://www.moonpage.com) - birthday year, month, and day can be passed into this 
# site's URL
#TODO: Include avg. gas price for birth year as a Birthday Fact
#TODO: Celebrities with the same b-day as a Birthday Fact
#TODO: Let user select timeframe (days) and have a dynamic table showing celebrities born within that timeframe
#TODO: Species extention as a b-day fact
#TODO: Most popular car, candy, etc. during birth year as b-day fact
#TODO: Let user pick their favorite sport and return the team who won the championship in their birth year