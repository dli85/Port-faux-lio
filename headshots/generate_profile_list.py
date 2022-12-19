from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from google.cloud import storage
import os
from PIL import Image
import concurrent.futures
from dataset import log_in

if __name__ == "__main__":
    studies = ['computer science', 'data science', 'electrical engineering', 'mechanical engineering']