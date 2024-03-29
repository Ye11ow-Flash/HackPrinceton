import requests
from bs4 import BeautifulSoup
import sys
import collections

# Get List of majors


def get_majors(url):
    majors = []
    desc = []
    data = []
    source_code = requests.get(url)
    plain_text = source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.findAll('a', {'class': 'accordion-title'}):
        majors.append(" ".join(link.text.split()))
    for link in soup.findAll('div', {'class': 'body columns small-12 large-6'}):
        temp = link.find('p').text
        desc.append(" ".join(temp.split()))

    for i in range(len(majors)):
        temp = []
        temp.append(majors[i])
        temp.append(desc[i])
        data.append(temp)

    return data


majors_list = get_majors("https://www.princeton.edu/academics/areas-of-study")
# for i in majors_list:
#     print(i)

# Get courses of a particular Major


def get_major_courses(url):
    major_course_list = []
    temp_list = []
    source_code = requests.get(url)
    plain_text = source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.findAll('div', {'class', 'columns small-12 medium-6 start'}):
        temp = []
        temp.append(link.find('strong').text)
        temp.append(link.find('h2').text)
        temp.append("Professor/Instructor: " + link.findAll('div')
                    [1].text.split("Professor/Instructor")[1])
        major_course_list.append(temp)
    i = 0
    for link in soup.findAll('div', {'class': 'views-field views-field-body columns small-12 medium-6'}):
        major_course_list[i].append(" ".join(link.text.split()))
        i += 1
    return major_course_list


major = "Computer Science"
major = major.lower()
major = major.replace(" ", "-")
url = "https://www.princeton.edu/academics/area-of-study/"+major
major_course_list = get_major_courses(url)
# for i in major_course_list:
#     print(i)

# Gets data of academic calender


def academic_calender(url):
    events = []
    source_code = requests.get(url)
    plain_text = source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    event_list = soup.find('div', {'class': 'item-list'})
    for link in event_list.findAll('li'):
        temp = []
        date = link.find('div', {'class': 'date-long'})
        temp.append(" ".join(date.text.split()))
        title = link.find('div', {'class': 'title'})
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
    plain_text = source_code.content
    soup = BeautifulSoup(plain_text, features="html.parser")
    for link in soup.findAll('div', {'class': 'card-section'}):
        temp = []
        name = link.find('h3').text
        temp.append(" ".join(name.split()))
        temp.append(" ".join(link.findAll('div')[1].text.split()))
        labs.append(temp)
    return labs


labs = get_labs("https://www.princeton.edu/research/facilities-labs")

# for i in events:
#     print(i)

# print(major_course_list[0][0])
# print(major_course_list[0][1])
# print(major_course_list[0][2])
# print(major_course_list[0][3])

# for i in major_course_list:
#     if "COS 326" in i[0]:
#         print(i)
# for i in majors_list:
#     print(i[0])
