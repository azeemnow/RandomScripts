########### CONFLUENCE KEYWORD SEARCH ###########

#OVERVIEW: This Python script is designed to search a Confluence server for specific keywords within pages or attachments. It interacts with the Confluence REST API to retrieve search results based on user-defined keywords and parameters. The script saves the search results in a CSV file for further analysis.

###You can customize the script by modifying the configuration parameters at the beginning of the script. For example, you can change the max_duration, keywords, and other parameters to match your specific search requirements.

###Feel free to tailor this script to your needs and use it to search for sensitive information or keywords within your Confluence instance.

#TO RUN THE SCRIPT: python confluence_search.py

#RESULTS STORAGE: The search results are saved in a CSV file named confluence_search_results.csv. The CSV file contains information about the pages or attachments that matched the specified keywords, including their titles, types, links, and the matched keyword.

#RATE LIMITING: The script is designed to adhere to Confluence rate limits. It limits the number of requests made per minute, as specified in the requests_per_minute variable. If you reach the rate limit, the script will wait for the next minute before making more requests.

#MAX RUN TIME: "max_duration" Sets the maximum duration for script execution in seconds. This determines how long the script will run before exiting This is a saftey control.

#SCRIPT STOPS: Once the search is complete or the maximum duration is reached, the script will exit, and it will display a message indicating where the results have been saved.

#FEEDBACK @azeemnow

###########

import requests
import json
import csv
import time
import getpass

# Prompt the user for their Confluence username and password
username = input("Enter your Confluence username: ")
password = getpass.getpass("Enter your Confluence password: ")

# Set the maximum duration for script execution (in seconds)
max_duration = 30  # Adjust this value as needed (e.g., 30 = 30seconds, 300 seconds = 5 minutes, )

# Record the start time
start_time = time.time()

# Set the hostname of the Confluence server
hostname = 'https://confluence.{Internal-Domain}.net'

# Set the search queries, content type, and field to search in
keywords = ['apikey', 'privateinfo', 'passwd', 'logindetails', 'creds', 'credz', 'passwords', 'credentails', 'password']


page_or_attach = 'attachment' 
# for searching attachments use full "attachment" 
text_or_title = 'text'

# Construct the CQL query with proper parameterization to search for either keyword

cql = f'(type={page_or_attach} AND ({text_or_title} ~ {keywords[0]} OR {text_or_title} ~ {keywords[1]} OR {text_or_title} ~ {keywords[2]} OR {text_or_title} ~ {keywords[3]} OR {text_or_title} ~ {keywords[4]} OR {text_or_title} ~ {keywords[5]} OR {text_or_title} ~ {keywords[6]} OR {text_or_title} ~ {keywords[7]} OR {text_or_title} ~ {keywords[8]}))'

 
# Construct the URL of the Confluence server's `/rest/api/content/search?` endpoint
url = f'{hostname}/rest/api/content/search?'

# Define the query parameters separately
params = {'cql': cql}

# Limit the number of requests per minute to 50. Per 2022 Confluence guideline, 500 requests per 5 minutes per user. 
requests_per_minute = 80
request_count = 0

# Make a GET request to the Confluence server with proper authentication and query parameters
while True:
    # Check if the maximum duration has been reached
    if time.time() - start_time >= max_duration:
        print(f'Maximum duration of {max_duration} seconds reached. Script is exiting.')
        break

    # Check if the request count has reached the limit
    if request_count >= requests_per_minute:
        # Calculate the time to wait for the next request
        time_to_wait = 60 - (time.time() - start_time) % 60
        if time_to_wait > 0:
            print(f'Waiting for {time_to_wait} seconds before making more requests...')
            time.sleep(time_to_wait)
            request_count = 0

    # Make the request
    response = requests.get(url, auth=(username, password), headers={'Accept': 'application/json'}, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        results = json.loads(response.content)

        # Specify the CSV file name
        csv_file_name = 'confluence_keyword_search_results.csv'

        # Open a CSV file for writing
        with open(csv_file_name, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Iterate over the results and write them to the CSV file
            for result in results['results']:
                # Determine which keyword was matched in the result
                matched_keyword = keywords[0] if f'{text_or_title} ~ {keywords[0]}' in cql else keywords[1]
                csv_writer.writerow([result["title"], result["type"], result["_links"]["webui"], matched_keyword])

        # Increment the request count
        request_count += 1

    else:
        # Print an error message with the status code and content
        print(f'Error: {response.status_code}\n{response.text}')

    # Add a delay between requests
    time.sleep(1)  # Adjust the delay as needed

print(f'Results saved to {csv_file_name}')
