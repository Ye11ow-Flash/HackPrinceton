import requests
from bs4 import BeautifulSoup
import sys
import collections

# course_title_data = []
# course_description = []
# course_classes = []
# course_prereq = []

# def get_course_list(url):
#     source_code = requests.get(url)
#     plain_text=source_code.content
#     soup = BeautifulSoup(plain_text, features="html.parser")
#     for link in soup.findAll("h2", {'class' : 'course-name'}):
#         temp = link.text.replace('\n', '')
#         course_title_data.append(" ".join(temp.split()))
#     for link in soup.findAll("div", {'class' : 'course-body'}):
#         desc = link.find('p')
#         if desc != None:
#             course_description.append(" ".join(desc.text.split()))
#         else:
#             course_description.append(None)
        
#         classes = link.find("div", {'class' : 'course-classes'})
#         if classes != None:
#             course_classes.append(" ".join(classes.text.split()))
#         else:
#             course_classes.append(None)

#         prereq = link.find("div", {'class', 'course-prereq'})
#         if prereq != None:
#             course_prereq.append(" ".join(prereq.text.split()))
#         else:
#             course_prereq.append(None)


# def get_all_pages(url):
#     source_code = requests.get(url)
#     plain_text=source_code.content
#     soup = BeautifulSoup(plain_text, features="html.parser")
#     pages = soup.find('ul', {'class' : 'pagination'})
#     counter = 0
#     for i in pages.findAll('li'):
#         counter += 1
#     no_of_pages = counter - 3
#     for i in range(no_of_pages):
#         get_course_list("https://www.cs.princeton.edu/courses/catalog?page="+str(i+1))    

# get_all_pages("https://www.cs.princeton.edu/courses/catalog")

def get_majors(url):
    # row small-collapse large-uncollapse accordion-item row ab undergraduate-certificate graduate-certificate
    majors = []
    source_code = requests.get(url)
    plain_text=source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.findAll('a', {'class' : 'accordion-title'}):
        majors.append(" ".join(link.text.split()))
    return majors


majors_list = get_majors("https://www.princeton.edu/academics/areas-of-study")

def get_major_courses(url):
    major_course_list = []
    source_code = requests.get(url)
    plain_text=source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.findAll('div', {'class', 'columns small-12 medium-6 start'}):
        temp = []
        temp.append(link.find('strong').text)
        temp.append(link.find('h2').text)
        temp.append("Professor/Instructor: " + link.findAll('div')[1].text.split("Professor/Instructor")[1])
        major_course_list.append(temp)
    return major_course_list

major = "Computer Science"
major = major.lower()
major = major.replace(" ", "-")
url = "https://www.princeton.edu/academics/area-of-study/"+major
major_course_list = get_major_courses(url)
for i in major_course_list:
    print(i)



#### This program scrapes naukri.com's page and gives our result as a
#### list of all the job_profiles which are currently present there.

# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

# #url of the page we want to scrape
# url = "https://www.naukri.com/top-jobs-by-designations# desigtop600"

# # initiating the webdriver. Parameter includes the path of the webdriver.
# driver = webdriver.Chrome('./chromedriver')
# driver.get(url)

# # this is just to ensure that the page is loaded
# time.sleep(5)

# html = driver.page_source

# # this renders the JS code and stores all
# # of the information in static HTML code.

# # Now, we could simply apply bs4 to html variable
# soup = BeautifulSoup(html, "html.parser")
# all_divs = soup.find('div', {'id' : 'nameSearch'})
# job_profiles = all_divs.find_all('a')

# # printing top ten job profiles
# count = 0
# for job_profile in job_profiles :
# 	print(job_profile.text)
# 	count = count + 1
# 	if(count == 10) :
# 		break

# driver.close() # closing the webdriver
