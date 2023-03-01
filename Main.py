from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import schedule, time

def book():
    driver = webdriver.Chrome()

    driver.get('https://libcal.law.uic.edu/booking/8thfloorcommons')
    dayMap = {"Sunday": 0, "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6}
    today = date.today()
    targetDay = date.today() +  timedelta(days = 7)
    currentMonth = today.strftime("%B")
    targetMonth = targetDay.strftime("%B")

    if currentMonth != targetMonth:
        try:
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='s-lc-rm-cal']/div/div/a[2]/span")))
            driver.find_element(By.XPATH, "//*[@id='s-lc-rm-cal']/div/div/a[2]/span").click()
        except:
            print("Forward arrow not found")
    
    dateInt = str(int(targetDay.strftime("%d")))
    dateString = targetDay.strftime("%A, %B") + " " + dateInt + ", " + targetDay.strftime("%Y")

    firstDay = targetDay.replace(day=1).strftime("%A")
    firstDate = dayMap[firstDay]
    day = int(targetDay.strftime("%d")) + firstDate
    row = int(day / 7 + 1)
    column = day % 7
    if day % 7 == 0: row = row - 1
    if column == 0: column = 7

    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='s-lc-rm-cal']/div/table/tbody/tr[%s]/td[%d]/a" % (row, column))))
        driver.find_element(By.XPATH, "//*[@id='s-lc-rm-cal']/div/table/tbody/tr[%s]/td[%d]/a" % (row, column)).click()
    except:
        print("Date not found")

    def getTime(t):
        ampm1 = "am"
        ampm2 = "am"
        time1 = t
        time2 = t + 1
        if (time1 >= 12): ampm1 = "pm"
        if (time2 >= 12): ampm2 = "pm"
        time1 = time1 % 12
        time2 = time2 % 12
        if (time2 == 0): time2 = 12
        if (time1 == 0): time1 = 12
        return str(time1) + ":00" + ampm1 + " to " + str(time2) + ":00" + ampm2 + ", "

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    weekends = ["Friday", "Saturday", "Sunday"]
    target = targetDay.strftime("%A")

    if target in weekdays:
        for t in range(17, 23):
            title = "S801 - Large Study Room, " + getTime(t) + dateString
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@title= '%s']" % (title))))
                driver.find_element(By.XPATH, "//*[@title= '%s']" % (title)).click()
                print("Selected: " + title)
            except:
                print("Could not select: " + title)
    elif target in weekends:
        for t in range(10, 21):
            title = "S801 - Large Study Room, " + getTime(t) + dateString
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//*[@title= '%s']" % (title))))
                driver.find_element(By.XPATH, "//*[@title= '%s']" % (title)).click()
                print("Selected: " + title)
            except:
                print("Could not select: " + title)

    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'rm_tc_cont')))
        driver.find_element(By.ID, 'rm_tc_cont').click()

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'fname')))
        driver.find_element(By.ID, 'fname').send_keys("FIRST NAME")

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'lname')))
        driver.find_element(By.ID, 'lname').send_keys("LAST NAME")

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element(By.ID, 'email').send_keys("EMAIL ADDRESS")

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 's-lc-rm-sub')))
        submitButton = driver.find_element(By.ID, 's-lc-rm-sub')
        submitButton.click()
        print("Booking Submitted")
    except:
        print("Could not book")

if __name__ == '__main__':

    schedule.every().day.at("00:00").do(book)
    while True:
        schedule.run_pending()
        time.sleep(1)
