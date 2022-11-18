import streamlit as st
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import math

st.title('Flats')
st.markdown("""This app retrieves apartmets in Bratislava based on the number of rooms""")
st.sidebar.header('Number of rooms')

# Number of pages:
r = requests.get(f'https://www.byty.sk/bratislava/3-izbove-byty/?p[param7]=12&p[limit]=60')
soup = BeautifulSoup(r.content, 'lxml')
pages = int(soup.find(class_= 'posledne box-no-shadow s').string)

# Empty list:
area_list = []

# Iteration over pages + scraping + cleanup + saving to list:
for page in range(1, pages + 1):
    r = requests.get(f'https://www.byty.sk/bratislava/3-izbove-byty/?p[param7]=12&p[limit]=60&p[page]={page}')
    soup = BeautifulSoup(r.content, 'lxml')

    items = soup.find_all('ul', class_='condition-info')
    for item in items:
        value = item.text.split('Novostavba ')[1].split('  m²')[0]
        try:
            area = float(value)
        except ValueError:
            pass
        area_list.append(float(area))

# Optional: sorting and printing values:
# area_list.sort()
# print(area_list)

# Defining bins for plot:
start = math.floor(min(area_list)/10)*10
end = math.ceil(max(area_list)/10)*10 + 10

# Histogram:
def histogram():
    fig = plt.figure()
    plt.hist(area_list, bins=np.arange(start, end, 10), ec = 'white')

    plt.xlabel('area in square meters')
    plt.ylabel('count')
    plt.title('3 room apartments')

    return st.pyplot(fig)
    # plt.savefig('3rooms.png')
    # plt.show()

if st.button('Show Plots'):
    histogram()