from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from control.ctr_converter import WAVConverter
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import urllib
import os
import random
import time
import subprocess
import pydub

def delay ():
    time.sleep(random.randint(2,3))

options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path='webdriver/chromedriver.exe')
driver.get("https://www.mangot5.com/Index/Member/Login?ref=/Index/Billing/couponList%3FcPage%3D1")


accountElement = driver.find_element_by_id("oldPassword")
accountElement.send_keys('')

passwordElement = driver.find_element_by_id("newPassword")
passwordElement.send_keys('')

frames=driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0]);
delay()

driver.find_element_by_class_name("recaptcha-checkbox-border").click()

driver.switch_to.default_content()
frames=driver.find_element_by_xpath("/html/body/div[4]/div[4]").find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[0])
delay()

driver.find_element_by_id("recaptcha-audio-button").click()

driver.switch_to.default_content()
frames= driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()

driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()
src = driver.find_element_by_id("audio-source").get_attribute("src")
print("[INFO] Audio src: %s"%src)
urllib.request.urlretrieve(src, os.getcwd()+"\\sample.mp3")

sound = pydub.AudioSegment.from_mp3(os.getcwd()+"\\sample.mp3")
sound.export(os.getcwd()+"\\sample.wav", format="wav")
sample_audio = sr.AudioFile(os.getcwd()+"\\sample.wav")

r= sr.Recognizer()

with sample_audio as source:
    audio = r.record(source)

key=r.recognize_google(audio)
print("[INFO] Recaptcha Passcode: %s"%key)

#key in results and submit
driver.find_element_by_id("audio-response").send_keys(key.lower())
driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
driver.switch_to.default_content()
delay()
driver.find_element_by_id("submitBtn").click()
delay()
