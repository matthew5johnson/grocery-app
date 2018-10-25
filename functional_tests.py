from selenium import webdriver

browser = webdriver.Firefox(keep_alive=False)
browser.get('http://localhost:8000')

assert 'Django' in browser.title