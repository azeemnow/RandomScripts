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
