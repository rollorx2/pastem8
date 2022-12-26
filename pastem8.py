import json
import os
import time
import re
import requests

# Set up a folder to store the data files
data_folder = 'data'
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Set up a folder to store the emailpass files
emailpass_folder = 'emailpass'
if not os.path.exists(emailpass_folder):
    os.makedirs(emailpass_folder)
    
# Set up a folder to store the upass files
upass_folder = 'upass'
if not os.path.exists(upass_folder):
    os.makedirs(upass_folder)

# Set up a list of regular expressions to match
regexes = [
    (re.compile(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+:[\w\d\!\@\#\$\%\^\&\*\(\)\_\+]{8,}'), 'emailpass'),
    (re.compile(r'[\w\d\!\@\#\$\%\^\&\*\(\)\_\+]+:[\w\d\!\@\#\$\%\^\&\*\(\)\_\+]{8,}'), 'upass')
]

while True:
    # Query the API
    response = requests.get('https://scrape.pastebin.com/api_scraping.php?limit=100')

    # Parse the JSON response
    pastes = json.loads(response.text)

    # Iterate over the pastes
    for paste in pastes:
        # Check if the paste has already been downloaded
        if os.path.exists(os.path.join(data_folder, paste['key'] + '.txt')):
            continue

        # Download the paste data
        paste_response = requests.get(paste['scrape_url'])
        paste_data = paste_response.text

        # Save the paste data to a file
        with open(os.path.join(data_folder, paste['key'] + '.txt'), 'w') as f:
            f.write(paste_data)

        # Check if the paste matches any of the regular expressions
        for regex, folder in regexes:
            if regex.search(paste_data):
                # Move the paste to the appropriate folder
                os.rename(os.path.join(data_folder, paste['key'] + '.txt'), os.path.join(folder, paste['key'] + '.txt'))
                break

    # Wait one minute before querying the API again
    time.sleep(60)
