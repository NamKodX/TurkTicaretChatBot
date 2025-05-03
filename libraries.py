# Standart Kütüphaneler
import base64
import json
import os
import re
import sys
import threading
import time
import tkinter as tk
import urllib.parse
from tkinter import filedialog
from urllib.parse import urljoin, urlparse

# Üçüncü Taraf Kütüphaneler
import nltk
import requests
import speech_recognition as sr
import webview
from bs4 import BeautifulSoup
from nltk.stem.snowball import SnowballStemmer
from selenium import webdriver
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.devtools.v133.css import take_computed_style_updates
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Matematiksel/Mantıksal Kütüphaneler
from sympy import And, Implies, Not, Or, symbols, to_cnf
