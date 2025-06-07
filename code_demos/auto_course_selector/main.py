# %% Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

account = ""
password = ""
# %% Start up
driver = webdriver.Edge()
driver.get("http://eamis.nankai.edu.cn/")

# %% Login
# Is there any better detection for the page to load?
account_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password_account_input"))
)
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "password_password_input"))
)
account_input.clear()
password_input.clear()
account_input.send_keys(account)
password_input.send_keys(password)
try:
    service_checkbox = driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'agreement-container') and .//span[contains(text(),'我已阅读并同意')]]//label[@class='arco-checkbox']",
    )
    service_checkbox.click()
except NoSuchElementException:
    pass

login_button = driver.find_element(By.XPATH, "//button[contains(., '登 录')]")
login_button.click()
# %% Direct to the course selection page
mine_menu = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[@id='menu_panel']/ul/li[./a[text()='我的']]")
    )
)
if (
    mine_menu.find_element(By.XPATH, "./a").get_attribute("class")
    != "first_menu active"
):
    mine_menu.click()
mine_menu.find_element(By.XPATH, ".//li[./a[text()='选课']]").click()
if "现在未到选课时间，无法选课！" in driver.page_source:
    print("现在未到选课时间，无法选课！")

input("Press Enter to exit...")
