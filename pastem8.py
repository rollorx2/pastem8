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
        if os.path.exists(os.path.join(data_folder, paste['key'] + '.txt')):
            continue

        # Download the paste data
        paste_response = requests.get(paste['scrape_url'])
        paste_data = paste_response.text

        # Save the paste data to a file, with the title as the first line
        filename = os.path.join(data_folder, paste['key'] + '.txt')
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(paste['title'] + '\n')
                f.write(paste_data)

            print(f'Saved paste {paste["key"]}')
        else:
            print(f'File {filename} already exists, skipping...')

        # Check if the paste matches any of the regular expressions
        # user_input = input('Do you want to perform the regex check? (y/n) ')
        # if user_input.lower() == 'y':
            # # Check if the paste matches any of the regular expressions
            # matched = False
            # for regex, folder in regexes:
                # if regex.search(paste_data):
                    # # Move the paste to the appropriate folder
                    # os.rename(os.path.join(data_folder, paste['key'] + '.txt'), os.path.join(folder, paste['key'] + '.txt'))
                    # print(f'Matched paste {paste["key"]} to {folder}')
                    # matched = True
                    # break
            
            # if not matched:
                # print(f'No match for paste {paste["key"]}')

    # Count the number of files in each folder
    emailpass_count = len(os.listdir(emailpass_folder))
    upass_count = len(os.listdir(upass_folder))
    print(f'Found {emailpass_count} emailpass files and {upass_count} upass files.')

    # Wait one minute before querying the API again
    print('Waiting 60 seconds...')
    for i in range(120):
        time.sleep(1)
        print(120 - i - 1, end='\r')
