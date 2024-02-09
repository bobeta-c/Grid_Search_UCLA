from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url_list = []

import sqlite3

con = sqlite3.connect("UCLA_BUILDING_STRUCTURE.db")
cur = con.cursor() #setup

cur.execute("SELECT * FROM buildings")
building_info = cur.fetchall()
for building in building_info:
    name = building[1]
    b_id = building[0]
    cur.execute("SELECT room_number FROM rooms WHERE building_id = ?", (b_id,)) #get all rooms in the building
    room_info = cur.fetchall()
    for room in room_info:
        url = "https://sa.ucla.edu/ro/Public/SOC/Results/ClassroomDetail?term=24W&classroom="
        room_number = room[0]
        room_number_saved = room[0]
        name_string = name
        name_string = name_string.replace(' ', '+')
        for i in range(8-len(name)):
            name_string += '+'
        room_first = ""
        room_last = ""
        if(room_number[0].isalpha()):
            if(room_number[1].isalpha()):
                room_first += room_number[0]
                room_first += room_number[1]
                room_number = room_number[2:]
            else:
                room_first += "+"
                room_first += room_number [0]
                room_number = room_number[1:]
        else:
            room_first = "++"
        if(room_number[-1].isalpha()):
            if(room_number[-2].isalpha()):
                room_last += room_number[-2]
                room_last += room_number[-1]
                room_number = room_number[:-2]
            else:
                room_last += room_number[-1]
                room_last += "+"
                room_number = room_number[:-1]
        else:
            room_last = "++"
        while(len(room_number) < 5):
            room_number = "0" + room_number

        url += name_string + "%7C" + room_first + room_number + room_last
        url_list.append((url, b_id, room_number_saved)) 


# Set up the Selenium WebDriver (make sure you have chromedriver installed)
for url_to_use in url_list:


    driver = webdriver.Chrome()
    driver.get(url_to_use[0])


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

    if result == []:
        driver.quit()
        continue
 
    room_num = url_to_use[2]
    bldg_id = url_to_use[1]

    cur.execute("SELECT id FROM rooms WHERE room_number = ? AND building_id = ?", room_num, bldg_id)
    room_id = cur.fetchone()
    if room_id:
        room_id = room_id[0]

        # Print the extracted content
        for i, fc_time_array in enumerate(result):
            times = fc_time_array[6:-7]
            start_time = times[:5].strip()
            end_time = times[7:].strip()
            start_time_i = minPastMid(start_time)
            end_time_i = minPastMid(end_time)
            
            cur.execute("INSERT INTO classes (start_time, end_time, room_id, quarter_id, day_of_week) VALUES (?, ?, ?, ?, ?)", (start_time_i, end_time_i, room_id, 1, i))

            #commit the changes
            con.commit()
            print(f"fc-event-container {i + 1}:")
            for fc_time in fc_time_array:
                print(f"  {fc_time}")

    else:
        print("ERROR")
    # Close the WebDriver
    driver.quit()

