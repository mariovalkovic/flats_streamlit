import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

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
area_list.sort()
print(area_list)

# Saving to csv:
df = pd.DataFrame(area_list, columns=["column"])
df.to_csv('3room.csv', index=False)