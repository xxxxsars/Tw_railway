# -*- coding: utf-8 -*-

import os,re,multiprocessing
os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
from TaiwanTrainVerificationCode2text import verification_code2text
import TaiwanTrainVerificationCode2text
PATH = TaiwanTrainVerificationCode2text.__path__[0]

from bs4 import BeautifulSoup
import cv2
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from PIL import Image
from datetime import datetime

import time

IDNumber = "A140043400"

class Railway:
    def __init__(self,disaply=False):

        if disaply:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])  # fix chrome safe issue
            chromedriver = r"/Users/mac/Python/chromedriver"  # chromedriver path
            self.driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
            self.driver.implicitly_wait(100)
        else:
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # define headless
            chromedriver = r"/Users/mac/Python/chromedriver"
            self.driver = webdriver.Chrome(executable_path=chromedriver,chrome_options=chrome_options)



        self.base_url = "http://railway.hinet.net/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def capcha_to_text(self,image_path):
        # capcha to text
        image = cv2.imread(image_path)
        text = verification_code2text.main(image)
        self.driver.find_element_by_id("randInput").clear()
        self.driver.find_element_by_id("randInput").send_keys(text)
        self.driver.find_element_by_id("sbutton").click()

    def booking(self):


        driver = self.driver
        driver.get(self.base_url + "/ctno1.htm")
        driver.maximize_window()

        # booking information
        driver.find_element_by_id("person_id").send_keys(IDNumber)
        Select(driver.find_element_by_id("from_station")).select_by_visible_text(u"106-桃園")
        Select(driver.find_element_by_id("to_station")).select_by_visible_text(u"175-台南")
        Select(driver.find_element_by_id("getin_date")).select_by_visible_text(u"2019/04/04【四】")
        driver.find_element_by_id("train_no").clear()
        driver.find_element_by_id("train_no").send_keys("111")
        Select(driver.find_element_by_id("order_qty_str")).select_by_visible_text(u"2")

        driver.find_element_by_css_selector("button[type=\"submit\"]").click()


        # retry capcha
        while True:
            # take screenshot
            image_path = 'captcha.png'
            element_img = self.driver.find_element_by_id('idRandomPic')
            left = element_img.location['x']
            top = element_img.location['y']
            right = element_img.location['x'] + element_img.size['width']
            bottom = element_img.location['y'] + element_img.size['height']
            self.driver.save_screenshot(image_path)
            im = Image.open(image_path)
            im = im.crop((left, top, right, bottom))
            im.save(image_path)
            self.capcha_to_text(image_path)

            # check capcha is valid
            soup = BeautifulSoup(driver.page_source, "html.parser")
            capcha_error_message = soup.find_all("p",{"class":"orange02"})


            if len(capcha_error_message) <1:
                break
            elif capcha_error_message[0] != "亂數驗證失敗":
                driver.find_element_by_xpath("/html/body/form/p[3]/input").click()

        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            result = soup.find("font", {"class", "orange02"}).text
            if result == "該區間無剩餘座位":
                print("Booking failed")
            elif result == "您的車票已訂到":
                booking_code = soup.find(id="spanOrderCode").text
                print("Booking sucessfully!!!\nYour person id %s\nYour booking code %s" % (IDNumber, booking_code))
        except AttributeError:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            above_quota =re.sub(":::|\n","",soup.find("body").text)
            if above_quota =="您(本乘車日)的訂票數超過 6 張。 同一乘車日訂票最多可訂 6 張票(但同時訂去回票者，最多可訂 12 張) 本乘車日您已訂票 6 張":
                print(above_quota)
                os._exit(0)



if __name__ == "__main__":
    while True:
        if datetime(2019, 3, 20, 00, 00, 00) == datetime.now().replace(microsecond=0):
            while True:
                try:
                    r = Railway()
                    p = multiprocessing.Pool()
                    for i in range(100):
                        p.apply_async(r.booking(),)
                    p.close()
                    p.join()
                except Exception as e:
                    break



