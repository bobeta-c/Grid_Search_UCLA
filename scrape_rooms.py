import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://sa.ucla.edu/ro/Public/Soc/search/classroomgridsearch"

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
    const classroomAutocomplete = shadow.querySelector("#classroom_autocomplete").shadowRoot;
    const dropdownItems = classroomAutocomplete.querySelector("#dropdownitems");

    const result = [];
    
    // Assuming the desired data is within a specific structure inside the dropdown items
    const items = dropdownItems.querySelectorAll('div[role="option"]'); // Adjust as needed
    
    items.forEach(item => {
        result.push(item.textContent.trim());
    });

    return result;
'''

result = driver.execute_script(script)

# Print the extracted content
for i, item in enumerate(result):
    print(f"Item {i + 1}: {item}")

# Close the WebDriver
driver.quit()

Rooms = {}
for item in result:
    Rooms[item[:9].strip()] =[]
for item in result:
    Rooms[item[:9].strip()] = Rooms[item[:9].strip()] + [item[9:]]


con = sqlite3.connect("random.db")
cur = con.cursor()

for x in Rooms.keys():
    building_name = x;

    cur.execute("SELECT id FROM buildings WHERE name = ?", (building_name,))
    building_id = cur.fetchone()

    if building_id:
        building_id = building_id[0]

        # Step 2: Insert a new row into the "rooms" table
        for room_number in Rooms[x]:

            cur.execute("INSERT INTO rooms (building_id, room_number) VALUES (?, ?)", (building_id, room_number))

            # Commit the changes to the database
            con.commit()
    else:
        print("building " + x + " not found")





con.close()



