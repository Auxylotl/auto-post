from time import sleep
import gspread
from PIL import Image, ImageDraw, ImageFont
from textwrap3 import wrap
from instabot import Bot
import os
import glob

counter = 0
#
me = gspread.service_account(filename="credss.json")
yes = me.open("testing")
ss = yes.worksheet("Form Responses 1")

username = "username"
password = "pass"
TEMPLATE = "path to base image here"
font = ImageFont.truetype("Consolas.ttf", size=48)
#
for file in os.listdir("./file where you put made images/"):
    os.remove(os.path.join("./file where you put made images/", file))


def login():
    try:
        c = glob.glob("config/*cookie.json") #deletes your login cookies
        os.remove(c[0])
    except:
        pass

    bot = Bot()
    bot.login(username=username, password=password)
    return bot


def makeimage(confess, template, to, fro):
    global counter
    counter += 1
    shadowcolor = "black"
    image = Image.open(template)
    image.resize((1080, 1080))
    draw = ImageDraw.Draw(image)
    wrapped = wrap(confess, width=30)
    draw.text(
        (25, 25), f"TO: {to}", font=ImageFont.truetype("Timesbd.ttf", size=48))
    draw.text(
        (25, 100), f"FROM: {fro}", font=ImageFont.truetype("Timesbd.ttf", size=48))
    for index, line in enumerate(wrapped):
        draw.multiline_text((200, 300+(75*index)), line, font=font)

    image.save(f"./file where you put made images/sus{counter}.jpeg")
    return str(counter)


def post(image, caption, bot):
    sleep(3)
    bot.upload_photo(image, caption=caption)


bot = login()

first = ss.get_all_records()
for i in range(10000000):
    print(len(first)+1)
    sleep(10)
    current = ss.get_all_records()
    print(len(current)+1)
    if len(current) > len(first):
        try:
            row = ss.row_values(len(current)+1)
            print(row)
            i = makeimage(row[1],
                          TEMPLATE, row[2], row[3]) #row [0] is timestamp (from google forms)
            post(f"./file where you put made images/sus{i}.jpeg", "make a caption here", bot)
        except:
            pass
    first = current
