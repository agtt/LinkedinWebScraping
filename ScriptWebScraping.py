import csv
import parameters
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector

# function to ensure all key data fields have a value
def validate_field(field):
    # if field is present pass if field:
    if field:
        pass
    # if field is not present print text else:
    else:
        field = 'No results'
    return field

linkedin_urls = []
# defining new  variable passing two parameters
writer = csv.writer(open(parameters.file_name, 'wb'))

# writerow() method to the write to the file object
writer.writerow(['Name', 'Job Title', 'Company', 'College', 'Location', 'URL'])

#Login Linkedin

driver = webdriver.Chrome('/home/rastap/Downloads/chromedriver_74/chromedriver')
driver.get('https://www.linkedin.com')

username = driver.find_element_by_class_name('login-email')
username.send_keys(parameters.linkedin_username)
sleep(0.5)


password = driver.find_element_by_class_name('login-password')
password.send_keys(parameters.linkedin_password)
sleep(0.5)

log_in_button = driver.find_element_by_class_name('submit-button')
log_in_button.click()

#Google Search
driver = webdriver.Chrome('/home/rastap/Downloads/chromedriver_74/chromedriver')
driver.get('https://www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
sleep(0.5)
search_query.send_keys(Keys.RETURN)
sleep(3)

while True:
    #Get Linkedin URLs
    get_linkedin_urls = driver.find_elements_by_tag_name('cite')
    get_linkedin_urls = driver.find_elements_by_class_name('iUh30')
    for url in get_linkedin_urls:
        linkedin_urls.append(url.text)
    sleep(1)
    next = driver.find_element_by_class_name('pn')
    if(next == ""):
        break
    next.click()

print(len(linkedin_urls))

# For loop to iterate over each URL in the list returned from the google search query
for linkedin_url in linkedin_urls:

    print("--> " + linkedin_url)

    # get the profile URL
    driver.get(linkedin_url)
    sleep(5)

    # assigning the source code for the web page to variable sel
    sel = Selector(text=driver.page_source)

    # xpath to extract the text from the class containing the name
    name = sel.xpath('//*[starts-with(@class, "pv-top-card-section__name")]/text()').extract_first()

    # if name exists
    if name:
        # .strip() will remove the new line /n and white spaces
        name = name.strip()

    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first()

    if job_title:
        job_title = job_title.strip()

    # xpath to extract the text from the class containing the company
    company = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__company-name")]/text()').extract_first()

    if company:
        company = company.strip()

    # xpath to extract the text from the class containing the college
    college = sel.xpath('//*[starts-with(@class, "pv-top-card-v2-section__entity-name pv-top-card-v2-section__school-name")]/text()').extract_first()

    if college:
        college = college.strip()

    # xpath to extract the text from the class containing the location
    location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()

    if location:
        location = location.strip()

    # assignment of the current URL
    linkedin_url = driver.current_url

    # validating if the fields exist on the profile
    name = validate_field(name)
    job_title = validate_field(job_title)
    company = validate_field(company)
    college = validate_field(college)
    location = validate_field(location)
    linkedin_url = validate_field(linkedin_url)

    # printing the output to the terminal
    print('\n')
    print('Name: ' + name)
    print('Job Title: ' + job_title)
    print('Company: ' + company)
    print('College: ' + college)
    print('Location: ' + location)
    print('URL: ' + linkedin_url)
    print('\n')

    # writing the corresponding values to the header
    # encoding with utf-8 to ensure all characters get loaded
    writer.writerow([name.encode('utf-8'),
                     job_title.encode('utf-8'),
                     company.encode('utf-8'),
                     college.encode('utf-8'),
                     location.encode('utf-8'),
                     linkedin_url.encode('utf-8')])

# terminates the application
driver.quit()