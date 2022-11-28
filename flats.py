import streamlit as st
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pandas import *
import plotly.express as px
import math

st.set_page_config(page_title='Apartments by size', layout='wide')

st.title('Apartments by size')
st.markdown("""This app is scraping sizes of new apartments for sale in Bratislava from byty.sk""")
st.sidebar.header('Options')
rooms = st.sidebar.slider('Rooms', min_value=1, max_value=4, value=3)
pages_scrape = st.sidebar.slider('Pages to Scrape', min_value=1, max_value=10, value=6)

# Empty data list:
my_bar = 0
my_text = 0
data_list = []
pages = 6

def scraper():
    # Cleaning old data:
    global data_list, rooms, pages
    data_list.clear()

    # Number of pages:
    r = requests.get(f'https://www.byty.sk/bratislava/{rooms}-izbove-byty/?p[param7]=12&p[limit]=60')
    soup = BeautifulSoup(r.content, 'lxml')
    pages_available = int(soup.find(class_= 'posledne box-no-shadow s').string)

    if pages_available < pages_scrape:
        pages = pages_available
    else:
        pages = pages_scrape

    # Iteration over pages + scraping + cleanup + saving to list:
    for page in range(1, pages + 1):
        r = requests.get(f'https://www.byty.sk/bratislava/{rooms}-izbove-byty/?p[param7]=12&p[limit]=60&p[page]={page}')
        soup = BeautifulSoup(r.content, 'lxml')

        items = soup.find_all('ul', class_='condition-info')
        for item in items:
            value = item.text.split('Novostavba ')[1].split('  m²')[0]
            try:
                area = float(value)
            except ValueError:
                pass
            data_list.append(float(area))
        
        # my_text.empty()
        global my_bar, my_text
        if my_bar != 0:
            my_bar.empty()
        # if my_text !=0:
        #     my_text.empty()
        
        my_text = ('Page ' + str(page) + ' done')
        my_bar = st.progress(0)
        # st.subheader(my_text)
        my_bar.progress(int(page/pages*100))

    # Optional: sorting and printing values:
    # area_list.sort()
    # print(area_list)

def histogram():
    global data_list, pages
    # Reading data:
    if len(data_list) == 0:
        data = read_csv('3room.csv')
        data_list = data['column'].tolist()
    else:
        pass

    # Graphics and ploting:
    fig = px.histogram(data_list, text_auto=True)
    fig.update_traces(marker=dict(color='rgb(0, 150, 255)'), textposition='inside')
    fig.update_layout(bargap=0.1, uniformtext_minsize=10, uniformtext_mode='hide', showlegend=False)
    return st.plotly_chart(fig)

default = st.checkbox('Show example', value = True)
load = st.sidebar.button('Scrape')

if default:
    histogram()
else:
    st.sidebar.header('Choose options and hit Scrape')

if load:
    scraper()
    histogram()


# save scraped df, open rollup of 4 different CSVs that are saved, add title to fig