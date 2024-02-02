import pygame
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
with open("./jacket.jpeg", "wb") as f:
    f.write(requests.get("""https://i.discogs.com/4TRqgbFq4dMcB1DU18LcnHtJ5MP8ljkl_bfnoI-PLv0/rs:fit/g:sm/q:40/h:300/w:300/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTI5MjQz/ODcyLTE3MDI5NzAw/NTktOTc1MS5qcGVn.jpeg""").content)