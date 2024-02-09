from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=24W&classroom=DODD++++%7C++00167++" 


# Set up the Selenium WebDriver (make sure you have chromedriver installed)

driver = webdriver.Chrome()
driver.get(url)

#divik is stupid as fuck

# Wait for the shadow DOM element to be present
try:
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, '#block-mainpagecontent div ucla-sa-soc-app'))
    WebDriverWait(driver, 10).until(element_present)
except TimeoutError:
    print("Timed out waiting for page to load")

# Execute JavaScript to find the desired element within the shadow DOM
script = '''
    const shadow = document.querySelector("#block-mainpagecontent > div > div > div > div > ucla-sa-soc-app").shadowRoot;
    const fcEventContainers = shadow.querySelectorAll(".fc-event-container");
    
    const result = [];
    
    fcEventContainers.forEach(container => {
        const fcTimeElements = container.querySelectorAll(".fc-time");
        const fcTimeArray = [];
        
        fcTimeElements.forEach(element => {
            fcTimeArray.push(element.innerHTML.trim());
        });
        
        result.push(fcTimeArray);
    });

    return result;
'''

result = driver.execute_script(script)

# Print the extracted content
for i, fc_time_array in enumerate(result):
    print(f"fc-event-container {i + 1}:")
    for fc_time in fc_time_array:
        print(f"  {fc_time}")

print(result)
# Close the WebDriver
driver.quit()

