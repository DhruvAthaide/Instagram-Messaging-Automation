from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import random

# Instagram Login Credentials
username = "lutapeho@yogrow.co"
password = "Scrapertest1234"

# XLSX file to read all user profiles provided
data = pd.read_excel("profile_links.xlsx", header=None, names=['Profile Links'])

profile_links = data['Profile Links'].tolist()

# XLSX file to store failed profile links
failed_profiles_file = "failed_profiles.xlsx"

# Create an empty DataFrame to store failed profile links
failed_profiles_df = pd.DataFrame(columns=['Profile Links'])

# Configuring the Chrome driver and making it Handling Notification Alert
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Opening the Instagram Website
driver.get("https://www.instagram.com/")

# Finding and Inputting the Username
username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'username'))
)
username_field.send_keys(username)

# Finding and Inputting the Password
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'password'))
)
password_field.send_keys(password)

# Finding and Clicking the Login Button
login_button = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
)
login_button.click()

# Time Delay to allow Login Process
time.sleep(7)

number = 1

# The script will randomly send any message from the array to each user profile
messages = [
    "Message 1",
    "Message 2",
    "Message 3",
    # Add more messages as needed
]

# Limit the number of messages sent in total and within a specific timeframe
max_messages = 50  # Set the max number of messages to not be detected as a bot
messages_sent = 0   # This is the variable for the number of messages sent total when the script is run
time_interval = 600  # Set the time interval in seconds

for profile_link in profile_links:
    try:
        if messages_sent >= max_messages:
            print("Stress test limit reached. Exiting...")
            break

        driver.get(profile_link)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body")))  # Wait for the page to load

        # XPath for the message button on the User Profile
        message_button_xpath = "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div"

        # Waiting and then clicking on the Message Button on the User Profile
        message_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, message_button_xpath))
        )
        message_button.click()

        # XPath for the message input field
        message_input_xpath = '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p'

        # Wait for the messaging popup to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, message_input_xpath))
        )

        # Finding the message input field using XPath
        msg = driver.find_element(By.XPATH, message_input_xpath)

        # Randomly selecting a message from the array to send to each user
        selected_message = random.choice(messages)

        for letters in selected_message:
            msg.send_keys(letters)
            time.sleep(random.uniform(0.1, 0.3))

        msg.send_keys(Keys.ENTER)
        print("Message sent to\t", profile_link)

        messages_sent += 1

        # Pause the script to avoid being detected as a bot
        time.sleep(random.uniform(3.2, 4.5))

        # Implemented time interval check with a random additional delay to not be detected as a bot
        if messages_sent % max_messages == 0:
            additional_delay = random.uniform(1, 60)  # Random number of seconds (1 to 60)
            total_delay = 240 + additional_delay  # 4 minutes + additional random seconds
            print(f"Waiting for {total_delay / 60} minutes to avoid detection...")
            time.sleep(total_delay)

    except Exception as e:
        print("Error sending message to", profile_link, ":", e)

        # All failed profiles are stored in the failed_profiles.xlsx file
        with open(failed_profiles_file, 'a') as file:
            file.write(profile_link + '\n')

        print(f"Profile link {profile_link} added to {failed_profiles_file}")

    print(number, "-----------------------------------------Msg_automate_kaux---------------------------------------------")
    number += 1

driver.quit()