# Visa det billigaste bensinpriset via bensinpriser.se.
import requests # pip install requests
import os
import json
from bs4 import BeautifulSoup # pip install BeautifulSoup4

r = requests.get('https://bensinpriser.nu/stationer/95/skane-lan/helsingborg')
soup = BeautifulSoup(r.text, "html.parser")

rowIndex = 0
for index, item in enumerate(soup.find_all('tr'), start=0):
    if index == 0: 
        continue
    # OKQ8 Välavägen
    if item.contents[1].contents[2] == 'Välavägen 27':
        pris95Okt = item.contents[3].contents[0].contents[0]
        datum     = item.contents[3].contents[2].contents[0]


# Convert to int
pris95Okt = pris95Okt.replace('kr','')  # ta bort 'kr'
pris95Okt = float(pris95Okt.replace(',','.'))  # , to .


# print("Pris: " + str(pris95Okt) + " den " + datum)

#-----------------------------------------------------------------------------
# Bil elförbrukning
avg_el_cosump = 25 # 25kwH/100km

# Bil bensinförbrukning
avg_b_consump = 10 # 10l/100km

cost = avg_b_consump * pris95Okt  # Kostnad per 100km

el_pris_threshold = cost / avg_el_cosump # allt över dyrare köra på el

result =  "EL_Th: " + str(el_pris_threshold) + " kr/kWh on " + datum 
# print("EL_Th: " + str(el_pris_threshold) + "kr/kWh")

file = 'result.json'
if os.path.exists(file):
    os.remove(file)

with open(file, 'a') as json_file:
    json.dumps(result, json_file)
