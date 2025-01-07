from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
import requests
import time

timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

#get the graph
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.spaceweatherlive.com/en/auroral-activity/kp-index.html") 
tree = etree.HTML(driver.page_source)
svg_element = tree.xpath('/html/body/div[2]/div/div/div[1]/div[4]/div[3]/svg')

# get the canvas
base_url = 'https://services.swpc.noaa.gov'
source_url = '/products/animations/enlil.json'
response = requests.get(base_url+source_url)
json_response = response.json()
img_urls = [(base_url+i['url']) for i in json_response]

# get the cactus data
cactus_url = 'https://www.sidc.be/cactus/out/cmecat.txt'
cactus_response = requests.get(cactus_url)
latest_cme = cactus_response.content.split(b'\n# \n#')[3]
latest_cme = str(latest_cme)[2:-1].split('\\n')

# making index page
html = etree.Element("html")
head = etree.SubElement(html, "head")
link = etree.SubElement(head, "link", rel="stylesheet", href="style.css")
script_element = etree.SubElement(head, "script", src="script.js")
title = etree.SubElement(head, "title")
title.text = "All CME at one place"

body = etree.SubElement(html, "body")
h1 = etree.SubElement(body, "h1")
h1.text = "Welcome to CME at a glance!"

p = etree.SubElement(body, "p")
p.text = "This page have all the CME data from various sources."

for svg in svg_element:
    body.append(svg)


img_container = etree.SubElement(body, "div", id='slider')       #"scroll-container")

image_elements = [etree.Element("img", id=f'img_{i}', class_='pic1', src=img_urls[i], width="960", height="600") for i in range(len(img_urls))]

for img in image_elements:
    img_container.append(img)

cme_table = etree.SubElement(body, "table", border="2")
lines = [etree.SubElement(cme_table, "tr", id=f'line{i}') for i in range(len(latest_cme))]
for col in latest_cme[0].split('|'):
        th = etree.SubElement(lines[0], 'th')
        th.text = col
for row in range(1, len(lines)):
    cols = latest_cme[row].split('|')
    for col in cols:
        td = etree.SubElement(lines[row], 'td')
        td.text = col

html_content = etree.tostring(html, pretty_print=True, method="html")
html_content = html_content.replace(b'class_', b'class')

filename = f"{timestamp}.html"
with open(filename, "wb") as file:
    file.write(html_content)

print(f"File saved as {filename}")



