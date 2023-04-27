import creds
import FormatEmailContent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict
import time
import datetime

driver = webdriver.Chrome()
url = 'https://www.healthhub.sg/'
driver.get(url)

def checkAppointmentSlot(duration, interval=1, *locations):
    healthHubLogin = '//*[@id="ctl00_ctl36_g_8b0826ba_6ba4_42f7_8dfb_ff4107b460f8_ctl00_CustomHeader"]/header/div/div[1]/div/div[2]/a[2]'
    passwordLogin = '//*[@id="SpQrToggle-1FATab"]'
    userId = '//*[@id="SpLoginIdPw-singpass-id"]'
    userPw = '//*[@id="SpLoginIdPw-password"]'
    loginButton = '//*[@id="SpLoginIdPw-login-button"]'

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, healthHubLogin)))
    driver.find_element(By.XPATH, healthHubLogin).click()

    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, passwordLogin).click()
    driver.find_element(By.XPATH, userId).send_keys(creds.username)
    driver.find_element(By.XPATH, userPw).send_keys(creds.password)
    driver.find_element(By.XPATH, loginButton).click()

    # Enter Otp here
    driver.implicitly_wait(10)
    otpInputBox = '//*[@id="SpTwoFaSms-otp-field"]'
    driver.find_element(By.XPATH, otpInputBox).click()
    while True:
        otpInput = driver.find_element(
            By.XPATH, otpInputBox).get_attribute('value')
        if len(otpInput) == 6:
            otpLoginButton = '//*[@id="SpTwoFaSms-submit-button"]'
            driver.find_element(By.XPATH, otpLoginButton).click()
            break
        time.sleep(0.5)

    try:
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, '//*[@id="btnProceed"]').click()
        print('Proceed clicked')
    except:
        print("No notification")

    WebDriverWait(driver, 60).until(EC.url_to_be(
        'https://eservices.healthhub.sg/PersonalHealth'))
    driver.get('https://eservices.healthhub.sg/Appointments/NewAppointment')
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[3]/div/article/div/div/div/div[2]/a')))
    driver.find_element(
        By.XPATH, '//*[@id="content"]/div[3]/div/article/div/div/div/div[2]/a').click()

    NHGP_Polyclinic = {'Ang Mo Kio': '//*[@id="polyclinicList"]/section[1]', 'Geylang': '//*[@id="polyclinicList"]/section[2]', 'Hougang': '//*[@id="polyclinicList"]/section[3]',
                       'Kallang': '//*[@id="polyclinicList"]/section[4]', 'Toa Payoh': '//*[@id="polyclinicList"]/section[5]', 'Woodlands': '//*[@id="polyclinicList"]/section[6]', 'Yishun': '//*[@id="polyclinicList"]/section[7]'}
    NUP_Polyclinic = {'Bukit Batok': '//*[@id="polyclinicList"]/section[1]', 'Bukit Panjang': '//*[@id="polyclinicList"]/section[2]', 'Choa Chu Kang': '//*[@id="polyclinicList"]/section[3]',
                      'Clementi': '//*[@id="polyclinicList"]/section[4]', 'Jurong': '//*[@id="polyclinicList"]/section[5]', 'Pioneer': '//*[@id="polyclinicList"]/section[6]', 'Queenstown': '//*[@id="polyclinicList"]/section[7]'}

    def findAppointmentSlots():
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(currentTime)

        slots = defaultdict(list)
        for location in locations:
            if location in NHGP_Polyclinic:
                driver.get(
                    'https://eservices.healthhub.sg/Appointments/NewAppointment/SelectPolyclinic?clusterCode=NHGP')

                # Select Polyclinic Location
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, NHGP_Polyclinic[location])))
                driver.find_element(
                    By.XPATH, NHGP_Polyclinic[location]).click()

            elif location in NUP_Polyclinic:
                driver.get(
                    'https://eservices.healthhub.sg/Appointments/NewAppointment/SelectPolyclinic?clusterCode=NUP')

                # Select Polyclinic Location
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, NUP_Polyclinic[location])))
                driver.find_element(By.XPATH, NUP_Polyclinic[location]).click()

            # Pick Service - Doctor consult
            drConsult = '//*[@id="serviceList"]/a[1]'
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, drConsult)))
            driver.find_element(By.XPATH, drConsult).click()

            # Click Continue
            buttonContinue = '//*[@id="content"]/div[2]/div/a'
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, buttonContinue)))
            driver.find_element(By.XPATH, buttonContinue).click()

            # Click No
            buttonNo = '//*[@id="content"]/div[2]/div[2]/a'
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, buttonNo)))
            driver.find_element(By.XPATH, buttonNo).click()

            # Checking for appointment slots
            driver.implicitly_wait(3)
            appointments = driver.find_elements(
                By.CLASS_NAME, 'list-select__item')

            if len(appointments) > 0:
                if len(appointments) == 1:
                    print(location, 'has 1 slot available.')
                else:
                    print(location, 'has', len(
                        appointments), 'slots available.')
                for appointment in appointments:
                    slots[location].append(appointment.text)
                    print(appointment.text)
            else:
                print(location, 'has no slot available.')

            # Click Cancel, start again
            cancelButton = '//*[@id="btnBack"]'
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, cancelButton)))
            driver.find_element(By.XPATH, cancelButton).click()

        if slots:
            FormatEmailContent.formatContent(slots)
            return True
        else:
            return False

    foundSlot = False
    loop = max(round(duration / interval), 1)
    while loop > 0:
        loop -= 1
        startTime = time.time()
        foundSlot = findAppointmentSlots()
        if foundSlot:
            print('Appointment slot(s) found, closing programme.')
            driver.quit()
            break
        scriptRunTime = time.time() - startTime
        if scriptRunTime >= 60*interval:
            continue
        time.sleep(60*interval - scriptRunTime)

    if not foundSlot:
        print('Appointment slot not found within',
              duration, 'mins. Closing programme.')
        driver.quit()


'''
Please enter the duration, time interval and location(s) you want to search for.
Example: checkAppointmentSlot(10, 1, 'Toa Payoh', 'Clementi', 'Woodlands')
'''
# Duration, interval, locations. Duration and interval in mins
checkAppointmentSlot(20, 1, 'Ang Mo Kio', 'Clementi', 'Geylang',
                     'Kallang', 'Choa Chu Kang', 'Toa Payoh', 'Bukit Batok')
