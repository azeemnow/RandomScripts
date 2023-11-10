import requests
import json
import csv
import time
import getpass

# Prompt the user for their Confluence username and password
username = input("Enter your Confluence username: ")
password = getpass.getpass("Enter your Confluence password: ")

# Print a message indicating the script is running
print("Searching for specified keywords in Confluence...")

# Set the maximum duration for script execution (in seconds)
max_duration = 300  # Adjust this value as needed (e.g., 300 seconds = 5 minutes, 30 = 30secs, 28800 seconds = 8hours)

# Record the start time
start_time = time.time()

# Set the hostname of the Confluence server
hostname = 'https://confluence.{DOMAIN}.net'

# Set the search queries, content type, and field to search in
keywords = ['logininfo', 'logindetails', 'mycredentials', 'passwords', 'credentials', 'credential', 'creds', 'credz', 'pass:', 'cred', 'password', 'apikey', 'pwd', 'secret', 'passwd', 'mypassword', 'privateinfo', 'passcode']

page_or_attach = 'attachment'  # Use attachment
text_or_title = 'text'

# Construct the CQL queries with proper parameterization to search for each keyword
cql_queries = []
for keyword in keywords:
    cql_queries.append(f'({text_or_title} ~ {keyword})')

cql = ' OR '.join(cql_queries)
cql = f'(type={page_or_attach} AND ({cql}))'

# Construct the URL of the Confluence server's `/rest/api/content/search` endpoint
url = f'{hostname}/rest/api/content/search?'

# Define the query parameters separately
params = {'cql': cql}

# Limit the number of requests per minute to 80. Per 2022 Confluence guideline, 500 requests per 5 minutes per user.
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
        csv_file_name = 'confluence_search_results.csv'

        # Open a CSV file for writing
        with open(csv_file_name, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Create a list of unique titles
            unique_titles = []

            # Iterate over the search results
            for result in results['results']:
                # Determine which keyword was matched in the result
                matched_keyword = keywords[0] if f'{text_or_title} ~ {keywords[0]}' in cql else keywords[1]

                # Check if the title has already been written
                if result["title"] not in unique_titles:
                    # Write the result to the CSV file
                    csv_writer.writerow([result["title"], result["type"], result["_links"]["webui"], matched_keyword])

    else:
        # Print an error message with the status code and content
        print(f'Error: {response.status_code}\n{response.text}')

    # Add a delay between requests
    time.sleep(1)  # Adjust the delay as needed

print(f'Results saved to {csv_file_name}')
