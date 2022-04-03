import random
import major_scrapper
import reference

# sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

# starter_encouragements = ["Cheer up!",
#                           "Hang in there.", "You are a great person / bot!"]

# def get_quote():
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text)
#     quote = json_data[0]['q'] + " -" + json_data[0]['a']
#     return(quote)

#################
# Client.event functions

# msg = message.content
# if message.content.startswith('$hello'):
#     await message.channel.send('Hello!')
# if message.content.startswith('$inspire'):
#     quote = get_quote()
#     await message.channel.send(quote)
# if any(word in msg for word in sad_words):
#     await message.channel.send(random.choice(starter_encouragements))

#################


def major_courses(major):
    url = "https://www.princeton.edu/academics/area-of-study/" + \
        major.lower().replace(" ", "-")
    return major_scrapper.get_major_courses(url)


def valid_department(department):
    try:
        return reference.courses[department.upper()]
    except:
        return "Invalid Department. Please try again."
