from flask import Flask, render_template, request
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
import time
import os

app = Flask(__name__)
db_config = {}
@app.route('/')
def index():
    return render_template('version4.html', message=None)
@app.route('/connect-database', methods=['POST'])
def connect_database():
    global db_config
    db_config = {
        "host": request.form['host'],
        "user": request.form['user'],
        "password": request.form['password'],
        "database": request.form['database']
    }
    try:
        mydb = mysql.connector.connect(**db_config)
        mydb.close()
        return render_template('version4.html', message="Connected successfully!")
    except mysql.connector.Error as e:
        return render_template('version4.html', message=f"Connection failed: {e}")
def get_webdriver(browser):
    try:
        if browser == "chrome":
            chrome_driver_path = r'D:\projects\mini project\multiple form filler\updated version of form filler\chrome-win64\chromedriver-win64\chromedriver.exe'
            if not os.path.exists(chrome_driver_path):
                return None, "Chrome WebDriver not found!"
            service = ChromeService(executable_path=chrome_driver_path)
            return webdriver.Chrome(service=service), None
        elif browser == "firefox":
            firefox_driver_path = r'D:\projects\mini project\multiple form filler\updated version of form filler\geckodriver-v0.36.0-win64\geckodriver.exe'
            if not os.path.exists(firefox_driver_path):
                return None, "Firefox WebDriver not found!"
            service = FirefoxService(executable_path=firefox_driver_path)
            return webdriver.Firefox(service=service), None
        else:
            return None, "Invalid browser selected!"
    except Exception as e:
        return None, str(e)
@app.route('/run-automation', methods=['POST'])
def run_automation():
    global db_config
    if not db_config:
        return render_template('version4.html', message="Database not connected!")

    try:
        mydb = mysql.connector.connect(**db_config)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT name, email, phone FROM user")
        user_info = cursor.fetchall()
        mydb.close()
    except mysql.connector.Error as e:
        return render_template('version4.html', message=f"Database error: {e}")

    browser = request.form['browser']
    form_url = request.form['form_url']

    driver, error = get_webdriver(browser)
    if driver is None:
        return render_template('version4.html', message=error)

    try:
        driver.get(form_url)
        for user in user_info:
            name_field = driver.find_element(By.ID,'name')
            name_field.clear()
            name_field.send_keys(user['name'])

            email_field = driver.find_element(By.ID,'email')
            email_field.clear()
            email_field.send_keys(user['email'])

            phone_field = driver.find_element(By.ID,'phone')
            phone_field.clear()
            phone_field.send_keys(user['phone'])
            waiting_time = int(request.form.get("waiting_time", 2))  
            time.sleep(waiting_time)  
            submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
            submit_button.click()
            driver.get(form_url)

        driver.quit()
        return render_template('version4.html', message="Form submitted successfully!")

    except Exception as e:
        driver.quit()
        return render_template('version4.html', message=f"Error filling form: {e}")
   


if __name__ == '__main__':
    app.run(debug=True)
