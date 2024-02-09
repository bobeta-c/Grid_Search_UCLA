from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=24W&classroom="


import sqlite3

con = sqlite3.connect("UCLA_BUILDING_STRUCTURE.db")
cur = con.cursor() #setup

cur.execute("SELECT * FROM buildings")
building_info = cur.fetchall()
for building in building_info:
    name = building[1]
    b_id = building[0]
    cur.execute("SELECT room_number FROM rooms WHERE building_id = ?", (b_id,)) #get all rooms in the building
    room_info = cur.fetchone()
    for room in room_info:
        room_number = room[0]
        name_string = name
        for i in range(8-len(name)):
            name_string += '#'
        room_string = "++00000++"
        if(room_number[0].isalpha()):
            if(room_number[1].isalpha()):
                room_string[0] = room_number[0]
                room = room
                room_string[1] = room_number[1]
                room_number = room_number[2:]
            else:
                room_string[1] = room_number[0]
                room_number = room_number[1:]
        if(room_number[-1].isalpha()):
            if(room_number[-2].isalpha()):
                room_string[-1] = room_number[-1]
                room_string[-2] = room_number[-2]
                room_number = room_number[:-2]
            else:
                room_string[-2] = room_number[-1]
                room_number = room_number[:-1]
        room_number = int(room_number)
        i = 0
        while(room_number > 0):
            room_string[6-i] = room_number % 10
            room_number = room_number//10
            i += 1

        url += name_string + "%7C" + room_string 
        print(url)
exit()
exit


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

