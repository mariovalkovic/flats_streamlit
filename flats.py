import streamlit as st
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pandas import *
import matplotlib.pyplot as plt
import math

st.title('Flats')
st.markdown("""This app retrieves apartments in Bratislava based on the number of rooms""")
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

    # Defining bins for plot:
    start = math.floor(min(data_list)/10)*10
    end = math.ceil(max(data_list)/10)*10 + 10

    # Graphics and ploting:
    fig = plt.figure()
    plt.hist(data_list, bins=np.arange(start, end, 10), ec = 'white')

    plt.xlabel('area in square meters')
    plt.ylabel('count')
    plt.title(str(rooms) + ' room apartments' + ' & ' + str(pages) + ' pages scraped')

    return st.pyplot(fig)
    # plt.savefig('3rooms.png')
    # plt.show()

default = st.checkbox('Show example', value = True)
load = st.sidebar.button('Scrape')

if default:
    histogram()
else:
    st.sidebar.header('Choose options and hit Scrape')

if load:
    st.markdown('I am scraping ' + str(pages) + ' pages right now. That is ' + str(pages*60) + ' flats')
    scraper()
    histogram()