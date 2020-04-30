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

def swap_loop(driver):
    """Runs the swapping behavior in a loop until the user quits the program."""

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
            get_input(driver)
        else:
            print("\nEnrollment successful! Congrats on getting into the waitlist for {0}.".format(COURSE_NAME))




def get_input(driver):
    """Gets input of whether or not the user wants to continue trying."""

    choice = raw_input("\nTry again? (Y/N) > ")
    if choice == 'Y':
        driver.switch_to.parent_frame()
        driver.find_element_by_id('PT_WORK_PT_BUTTON_BACK').click()
        swap_loop(driver)
    elif choice == 'N':
        driver.quit()
    else:
        print("Invalid choice.")
        get_input(driver)

def enroll():
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
    driver_options.add_argument('log-level=3')
    driver_options.headless = HEADLESS

    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe",
        options=driver_options)

    if auth_calnet(driver):
        swap_loop(driver)
    else:
        print("Authentication failed. Quitting this application...")
        driver.quit()

if __name__ == "__main__":
    enroll()
