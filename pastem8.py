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
    (re.compile(r'^[a-z0-9]{6,20}:[a-zA-Z0-9!@#$%^&*()]{8,14}$'), 'emailpass'),
    (re.compile(r'(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6011[0-9]{12}|3(?:0[0-5]|[68][0-9])[0-9]{11}|3[47][0-9]{13})'), 'credit_card'),
    (re.compile(r'\b[\w\d\!\@\#\$\%\^\&\*\(\)\_\+]{5,20}:[\w\d\!\@\#\$\%\^\&\*\(\)\_\+]{8,}\b'), 'upass')
]

while True:
    # Query the API
    print('Querying the API...')
    response = requests.get('https://scrape.pastebin.com/api_scraping.php?limit=100')

    # Parse the JSON response
    pastes = json.loads(response.text)

    # Iterate over the pastes
    for paste in pastes:
        # Check if the paste has already been downloaded
        filename = os.path.join(data_folder, paste['key'] + '.txt')
        if not os.path.exists(filename):
            # Download the paste data
            paste_response = requests.get(paste['scrape_url'])
            paste_data = paste_response.text

            # Save the paste data to a file, with the title as the first line
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(paste['title'] + '\n')
                f.write(paste_data)

            print(f'Saved paste {paste["key"]}')
        else:
            print(f'File {filename} already exists, skipping...')
        # Check if the paste matches any of the regular expressions
        matched = False
        for regex, folder in regexes:
            if regex.search(paste_data):
                # Move the paste to the appropriate folder
                destination = os.path.join(folder, paste['key'] + '.txt')
                if os.path.exists(destination):
                    # If the destination file already exists, skip the current iteration
                    continue

                os.rename(filename, destination)
                print(f'Matched paste {paste["key"]} to {folder}')
                matched = True
                break

    # Pause for a 240 seconds 
    time.sleep(240)

