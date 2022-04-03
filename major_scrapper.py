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

# Get List of majors
def get_majors(url):
    majors = []
    desc = []
    data = []
    source_code = requests.get(url)
    plain_text=source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.findAll('a', {'class' : 'accordion-title'}):
        majors.append(" ".join(link.text.split()))
    for link in soup.findAll('div', {'class' : 'body columns small-12 large-6'}):
        temp = link.find('p').text
        desc.append(" ".join(temp.split()))
    
    for i in range(len(majors)):
        temp = []
        temp.append(majors[i])
        temp.append(desc[i])
        data.append(temp)

    return data


majors_list = get_majors("https://www.princeton.edu/academics/areas-of-study")
for i in majors_list:
    print(i)

# Get courses of a particular Major
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

# Gets data of academic calender
def academic_calender(url):
    events = []
    source_code = requests.get(url)
    plain_text=source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    event_list = soup.find('div', {'class' : 'item-list'})
    for link in event_list.findAll('li'):
        temp = []
        date = link.find('div', {'class' : 'date-long'})
        temp.append(" ".join(date.text.split()))
        title = link.find('div', {'class' : 'title'})
        temp.append(" ".join(title.text.split()))
        events.append(temp)
    return events

url = "https://registrar.princeton.edu/academic-calendar-and-deadlines"
all = "?audience[216]=216&audience[211]=211&audience[206]=206"
ug = "?audience[206]=206"
grad = "?audience[211]=211"
faculty = "?audience[216]=216"
pg = "&page=1"
input = all
type = "0"
if type == "ug":
    url += ug + pg
elif type == "grad":
    url += grad + pg
elif type == "faculty":
    url += faculty + pg
else:
    url += all + pg
events = academic_calender(url)

# Various Facilities and Labs
def get_labs(url):
    labs = []
    source_code = requests.get(url)
    plain_text=source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.findAll('div', {'class' : 'card-section'}):
        temp = []
        name = link.find('h3').text
        temp.append(" ".join(name.split()))
        temp.append(" ".join(link.findAll('div')[1].text.split()))
        labs.append(temp)
    return labs

labs = get_labs("https://www.princeton.edu/research/facilities-labs")    

# for i in events:
#     print(i)