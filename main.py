import discord
import requests
import json
import major_scrapper
import reference
import private
import helpers
from discord.ext import commands

client = commands.Bot(command_prefix="$")


# @client.command()
# async def embed(ctx):
#     embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
#                           description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)

#     embed.set_footer(text="this is a footer")
#     embed.set_image(
#         url="https://upload.wikimedia.org/wikipedia/commons/1/15/Princeton_Tigers_logo.png")
#     embed.set_thumbnail(
#         url="https://upload.wikimedia.org/wikipedia/commons/1/15/Princeton_Tigers_logo.png")
#     embed.set_author(name="Michael")
#     embed.add_field(name="field name", value="field value", inline=False)
#     embed.add_field(name="field name", value="field value", inline=True)
#     embed.add_field(name="field name", value="field value", inline=True)
#     await ctx.send(embed=embed)


# @commands.command()
# async def hello(ctx):
#     await ctx.send("hello world")

# client.add_command(hello)


# @client.command()
# async def embed(ctx):
#     embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
#                           description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
#     await ctx.send(embed=embed)


@client.event
async def on_read():
    # 0 gets replaced with client
    print('We have logged in as {0.user}.format(client)')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # title="Princeton CourseBot",
    embed = discord.Embed(color=discord.Color.dark_orange())
    # description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    embed.set_author(name="Princeton CourseBot",
                     icon_url="https://i0.wp.com/blogs.princeton.edu/mudd/wp-content/uploads/sites/41/2013/03/TigerHead.jpg")
    embed.set_footer(text="Run [$help] to get all the commands for this bot.")
    if message.content.startswith('$department '):
        parse = ''.join(message.content.split(
            "$department ")).split(" ")
        name = helpers.valid_department(parse[0])
        embed.add_field(name="Department Name", value=name, inline=True)
        if "Invalid" not in name:
            embed.add_field(name="Course Roster", value="Link: " + "https://www.princeton.edu/academics/area-of-study/" +
                            name.lower().replace(" ", "-"), inline=True)
            description = ""
            for i in major_scrapper.majors_list:
                if name.split(" ")[0] in i[0]:
                    description = i[1]
            embed.add_field(name="Description: ",
                            value=description, inline=False)
        elif "all" in parse:
            all_department_names = ""
            for i in reference.courses.keys():
                all_department_names += i + "; "
            embed.add_field(name="All Department Names",
                            value=all_department_names, inline=False)
        embed.add_field(
            name="Tip", value="Try `$department all` to get all department abbreviations.", inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith('$class '):
        poll = ''.join(message.content.split("$class ")).split(" ")
        name = poll[0] + " " + poll[1]
        department = reference.courses[poll[0]]
        courses = helpers.major_courses(department)
        course = ""
        for i in courses:
            if name in i[0]:
                course += "Department: " + department + "\n" + \
                    "Course Number: " + poll[1] + "\n" + \
                    "Course Name: " + i[1] + "\n" + \
                    i[2] + "\n" + \
                    "Description: " + i[3]
                embed.add_field(name="Department",
                                value=department, inline=False)
                embed.add_field(name="Course Number",
                                value=poll[1], inline=False)
                embed.add_field(name="Course Name",
                                value=i[1], inline=False)
                embed.add_field(name="Professor/Instructor",
                                value=i[2].split(": ", 1)[1], inline=False)
                embed.add_field(name="Description",
                                value=i[3], inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith('$major '):
        poll = ''.join(message.content.lower().split("$major "))
        majors = major_scrapper.get_majors(
            "https://www.princeton.edu/academics/areas-of-study")
        classes = ""
        classes_one = ""
        classes_two = ""
        classes_three = ""
        cnt = 0
        embed.add_field(name="Major",
                        value=poll, inline=False)
        if poll == "all":
            for i in majors:
                if "Engineering" in i[0]:
                    i[0] = i[0].replace("Engineering", "Eng")
                if "and" in i[0]:
                    i[0] = i[0].replace("and", "&")
                if cnt < 33:
                    classes_one += i[0] + ", "
                elif cnt < 66:
                    classes_two += i[0] + ", "
                else:
                    classes_three += i[0] + ", "
                cnt += 1
            embed.add_field(name="All Areas of Study",
                            value=classes_one, inline=False)
            embed.add_field(name="All Areas of Study (Cont.)",
                            value=classes_two, inline=False)
            embed.add_field(name="All Areas of Study (Cont.)",
                            value=classes_three, inline=False)
        else:
            cnt = 0
            courses = helpers.major_courses(poll)
            for i in courses:
                if cnt < round(len(courses)/2):
                    classes_one += i[0] + " " + i[1] + "\n"
                else:
                    classes_two += i[0] + " " + i[1] + "\n"
                cnt += 1
            embed.add_field(name="Major Courses",
                            value=classes_one, inline=False)
            embed.add_field(name="Major Courses (Cont.)",
                            value=classes_two, inline=False)
        embed.add_field(name="Tip",
                        value="Type `$major [area name]` to get all courses in given area. Type `$major all` to get all areas of study.", inline=False)
        await message.channel.send(embed=embed)
    if message.content.startswith("$help"):
        embed.add_field(name="Department",
                        value="Type `$department all` to get all department abbreviations. Type `$department [department abbrev.]` to get a description of that department.", inline=False)
        embed.add_field(name="Class",
                        value="Type `$class [Department Name] [Class Number]` to get information about a given class.", inline=False)
        embed.add_field(name="Major",
                        value="Type `$major all` to get all areas of study. Type `$major [department name] to get all courses listed for that area.", inline=False)
        embed.add_field(name="Calendar",
                        value="Type `$calendar` to get the dates and descriptions of upcoming events.", inline=False)
        embed.add_field(name="Help",
                        value="Type `$help` to get all commands for this bot.", inline=False)
        embed.add_field(name="Bot Invite Link",
                        value="https://discord.com/api/oauth2/authorize?client_id=959889388639240203&permissions=534723946560&scope=bot", inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("$calendar"):
        events_one = ""
        events_two = ""
        events_three = ""
        cnt = 0
        for i in major_scrapper.events:
            if cnt < round(len(major_scrapper.events)/3):
                events_one += i[0].split(": ", 1)[1] + ": " + i[1] + "\n"
            elif cnt < round(len(major_scrapper.events)*2/3):
                events_two += i[0].split(": ", 1)[1] + ": " + i[1] + "\n"
            else:
                events_three += i[0].split(": ", 1)[1] + ": " + i[1] + "\n"
            cnt += 1
        embed.add_field(name="Calendar",
                        value=events_one, inline=False)
        embed.add_field(name="Calendar (Cont.)",
                        value=events_two, inline=False)
        embed.add_field(name="Calendar (Cont.)",
                        value=events_three, inline=False)
        await message.channel.send(embed=embed)


# @client.command()
# async def displayembed():
#     embed = discord.Embed(
#         title="Title",
#         description="This is a description.",
#         color=discord.Color.orange()
#     )

#     embed.set_footer(text="this is a footer")
#     embed.set_image(
#         url="https://irs.princeton.edu/sites/g/files/toruqf276/themes/site/logo.svg")
#     embed.set_thumbnail(
#         url="https://irs.princeton.edu/sites/g/files/toruqf276/themes/site/logo.svg")
#     embed.set_author(name="Michael")
#     embed.add_field(name="field name", value="field value", inline=False)
#     embed.add_field(name="field name", value="field value", inline=True)
#     embed.add_field(name="field name", value="field value", inline=True)

#     await client.say(embed=embed)


# runs bot
client.run(private.get_token())
