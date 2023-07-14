import csv
import requests
from bs4 import BeautifulSoup
import time
import os
import argparse

def get_links(url, output_directory):
    data = []
    # Iterate over pages
    for page in range(1, max_pages+1):
        url_next = f"{url}liste/page/{page}"
        response = requests.get(url_next)
        
        txt = BeautifulSoup(response.content, "html.parser")
        containers = txt.find_all('aside', class_='contenu_annonce')
        
        for container in containers: 
            link = container.find('a')['href']
            job_title = container.find('strong').text.strip()
            company_name = container.find('h4').text.strip()
            contrat = container.find('h5').text.strip()
            desc = container.find(class_='description').text.strip()
            
            
            data.append([link + '\t' + job_title + '\t' + contrat + '\t' + company_name  + '\t' + desc ])
        
    # Sleep for 1 second before processing the next page
    current_time = time.sleep(1)
    print("Sleep time:", current_time)   
    
    # Save URLs to a CSV file and join the file with the current directory
    filename = os.path.join(output_directory, "extract.tab")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Link' + '\t' +'Job Title' + '\t' +'Contrat' + '\t' +'Company Name' + '\t' +'Description'])
        writer.writerows(data)
                
    print(f"URLs and job titles saved to {filename} successfully.")

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--output_directory', type=str, required=True, help='Output directory')
args = parser.parse_args()

# Create the output directory if it doesn't exist
os.makedirs(args.output_directory, exist_ok=True)

# Url Start
url = "https://www.portaljob-madagascar.com/emploi/"
max_pages = 5

start_time = time.time()
get_links(url, args.output_directory)
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds.")
