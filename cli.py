## The CLI interface for the Dining
## Pts application.

import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ExpCond
from selenium.webdriver.common.by import By

from six.moves import input as raw_input

from constants import *
from cal_auth import auth_calnet
from menu import menu_loop

def swap_loop():
    # navigate to the swap page
    driver.switch_to.frame(0)
    n = 0
    radio_btn = None

    while radio_btn is None and n < 5:
        term_texts = driver.find_elements_by_id('TERM_CAR${0}'.format(n))
        if len(term_texts) > 0 and term_texts[0].text == TERM:
            radio_btn = driver.find_element_by_id('SSR_DUMMY_RECV1$sels${0}$$0'.format(n))
        else:
            n += 1

    radio_btn.click()
    driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO').click()

    # find the courses and select them

    WebDriverWait(driver, 10).until(ExpCond.presence_of_element_located((By.ID, 'DERIVED_REGFRM1_DESCR50$225$')))
    swap_selected, course_selected = False, False

    swap_dropdown = driver.find_element_by_id('DERIVED_REGFRM1_DESCR50$225$')
    for option in swap_dropdown.find_elements_by_tag_name('option'):
        if SWAP_NAME in option.text:
            print('Selected {0} to swap'.format(option.text))
            option.click()
            swap_selected = True
    
    course_dropdown = driver.find_element_by_id('DERIVED_REGFRM1_SSR_CLASSNAME_35$183$')
    for option in course_dropdown.find_elements_by_tag_name('option'):
        if COURSE_NAME in option.text:
            print('Selected {0} to enroll'.format(('' + option.text).replace('\n', ' ')))
            option.click()
            course_selected = True

    if not swap_selected:
        print("ERROR: Course {0} not found in your enrolled classes!".format(SWAP_NAME))
    elif not course_selected:
        print("ERROR: Course {0} not found in your shopping cart!".format(COURSE_NAME))
    else:
        # Wait until enroll page is loaded
        driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_ADDTOLIST1$184$').click()
        WebDriverWait(driver, 10).until(ExpCond.presence_of_element_located((By.ID, 'DERIVED_REGFRM1_SSR_PB_SUBMIT')))
        # Wait until confirmation message appears
        driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_SUBMIT').click()
        WebDriverWait(driver, 10).until(ExpCond.presence_of_element_located((By.ID, 'DERIVED_REGFRM1_DESCR1$8$')))
        message_xpath = '/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[9]/td[2]/div/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div'
        if 'no available seats' in driver.find_element_by_xpath(message_xpath).text:
            print("\nClass is full! Enrollment was unsuccessful.")
            get_input()
        else:
            print("\nEnrollment successful! Congrats on getting into the waitlist for {0}.".format(COURSE_NAME))

    


def get_input():
    """Gets input of whether or not the user wants to continue trying."""

    choice = raw_input("Try again? (Y/N) > ")
    if choice == 'Y':
        driver.switch_to.parent_frame()
        driver.find_element_by_id('PT_WORK_PT_BUTTON_BACK').click()
        swap_loop()
    elif choice == 'N':
        driver.quit()
    else:
        print("Invalid choice.")
        get_input()


###########################################################


print("""
======================================================
|              Full Waitlist Enroller                |
|                  by 64bitpandas                    |
|                  version 0.0.1                     |
======================================================
""")

if (not DISABLE_WARNING):
    print("""
    >> NOTICE!
    This program is still in development.
    Unintended behavior may result from the use of this program.
    Further usage of this program means that you run this program at your own risk.

    IMPORTANT: DO NOT TRUST YOUR PERSONAL DATA IN THE WRONG HANDS!
    Always double check the source code of what you are running.
    You may safely quit this application through CTRL+C.

    To disable this warning, edit the DISABLE_WARNING flag in constants.py.
    """)

driver_options = webdriver.ChromeOptions()
driver_options.add_argument("--ignore-certificate-errors-spki-list")
driver_options.add_argument("--ignore-ssl-errors")
driver_options.headless = False

driver = webdriver.Chrome(
    executable_path="./chromedriver.exe",
    options=driver_options)

if auth_calnet(driver):
    swap_loop()
else:
    print("Authentication failed. Quitting this application...")
    driver.quit()






    # print(driver.current_url)
    # # print(driver.find_element_by_xpath("/html/body/form/div[5]/table/tbody/tr/td/div/table/tbody/tr[4]/td[2]/div/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/div/input"))
    # inputs = driver.find_element(By.XPATH, '//*[@id="TERM_CAR${0}"]'.format(2))
    # for input in inputs:
    #     print(input, "INPUT")
    #     term = input.find_element_by_xpath('./../../../td[1]/div/span')
    #     # term = input.find_element_by_xpath('./../..')
    #     print(term)
    #     print(term.text)

    # terms = driver.find_elements_by_xpath('//div[contains(text(), "{0}") and @class="inner"]'.format(TERM))
   
    # print("Loading balances from Cal Dining and Housing...")
    # driver.get(URL_BALANCES_PORTAL)

    # btn_view_bal = "html/body/div/div[3]/div/div/div/div[1]/div/div[3]/a"

    # WebDriverWait(driver, 3).until(
    #     ExpCond.element_to_be_clickable((By.XPATH, btn_view_bal))
    # )

    # driver.find_element(By.XPATH, btn_view_bal).click()
    
    # # This is specific to a certain configuration.
    # txt_sid = "/html/body/div/div[3]/div/div/div/div[2]/div/table/tbody/tr[3]/td/b"
    # txt_flex = "/html/body/div/div[3]/div/div/div/div[2]/div/table/tbody/tr[7]/td[1]/b"

    
    # def get_txt(xpath):
    #     elem = driver.find_element(By.XPATH, xpath)
    #     return elem.text

    # print("============ STUDENT INFO ============")
    # print("Your student ID is " + get_txt(txt_sid))

    # if len(driver.find_elements(By.XPATH, txt_flex)) > 0:
    #     print("Your remaining flex dollars: " + get_txt(txt_flex))
    #     menu_loop(driver)
    # else:
    #     print("Unfortunately, you are not on a meal plan.")
    #     print("This application cannot provide much information...")
    
    # driver.quit()



