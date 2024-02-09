from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=24W&classroom=DODD++++%7C++00167++"

# Set up the Selenium WebDriver (make sure you have chromedriver installed)
driver = webdriver.Chrome()
driver.get(url)

# Wait for the shadow DOM element to be present
try:
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '#block-mainpagecontent div ucla-sa-soc-app'))
    WebDriverWait(driver, 10).until(element_present)
except TimeoutError:
    print("Timed out waiting for page to load")

# Execute JavaScript to find the desired element within the shadow DOM
script = '''
    const shadow = document.querySelector("#block-mainpagecontent > div > div > div > div > ucla-sa-soc-app").shadowRoot;
    const desiredElement = shadow.querySelector("#calendar > div > div > table > tbody > tr > td > div > div > div.fc-content-skeleton > table > tbody > tr");
    return desiredElement.innerHTML;
'''

desired_element_html = driver.execute_script(script)


# Print the extracted content
print(desired_element_html)

# Close the WebDriver
driver.quit()

