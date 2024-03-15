import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from datetime import datetime

"""
# Stormlight Reread Calculator
Enter a start date and receive a reading schedule.
"""
start_date = datetime.combine(st.date_input(label="Start Date", min_value=datetime.now()), datetime.min.time())

end_date = datetime.strptime('12/06/2024', '%m/%d/%Y')


days_to_read = (end_date-start_date).days
weeks_to_read = round(days_to_read/7, 0)

st.write('Start Date: {}'.format(start_date))
st.write('Days to Read: {}'.format(days_to_read))
st.write('Weeks to Read: {}'.format(weeks_to_read))

def remove_comma(val):
    return val.replace(',', '')

# Read in data
df = pd.read_csv('stormlight_data.csv')

# Make the word count a number
df['word_count'] = pd.to_numeric(df['word_count'].apply(func=remove_comma))

# Calculate words per week based on how many weeks we have
words_per_week = df['word_count'].sum()/weeks_to_read
st.write('Words per Week: {}'.format(words_per_week))

# Add a book number column
title_map = {
    'The Way of Kings': 1,
    'Words of Radiance': 2,
    'Oathbringer': 3,
    'Rhythm of War': 4
}
df.insert(loc=0,
        column = 'book_number',
        value = df['book'].map(title_map))


chap = df.groupby(['book_number', 'chapter_num']).agg({'word_count': 'sum', 'chapter_title': 'max', 'pov': ', '.join})

chap['running_word_count'] = chap['word_count'].cumsum()


for i in range(0,int(weeks_to_read)):
    chap.loc[
            (chap['running_word_count'] > i*words_per_week) 
            & 
            (chap['running_word_count'] <= (i+1)*words_per_week)
        , 'week_date'] = start_date + timedelta(days=(i*7))

st.dataframe(chap)