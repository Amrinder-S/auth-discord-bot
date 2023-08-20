import discord
import json
import random
import re
import os
import ssl
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#global variables
GNDEC_DISCORD_ID = 1123068128834899998
GNDEC_LOGS_CHANNEL = 1142833474185744465
ROLE_FIRST_YEAR = 1123938097957191810
ROLE_SECOND_YEAR = 1123938146141347860
ROLE_THIRD_YEAR = 1124275055749251092
ROLE_FOURTH_YEAR = 1124275287648112700

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
codes = {}

async def sendMessage(guild_id, channel_id, message): # function to send messages.
    guild = client.get_guild(guild_id)
    joinCh = discord.utils.get(guild.text_channels, id=channel_id)
    await joinCh.send(message)

async def sendEmail(sender_email, receiver_email, subject, message):
    print("attempting to send email.")
    sender_password = os.environ.get('SENDGRID_PASSWORD') #sendgrid password (to be stored in enviornment variables. on windows: setx SENDGRID_PASSWORD PASSWORD_GOES_HERE)
    smtp_server = 'smtp.sendgrid.net'
    smtp_port = 465
    try:
        session = smtplib.SMTP_SSL(smtp_server, smtp_port)
        session.login("apikey", sender_password)
        msg = f'From: {sender_email}\r\nTo: {receiver_email}\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: {subject}\r\n\r\n'
        msg += message
        session.sendmail(sender_email, receiver_email, msg.encode('utf8'))
        session.quit()
        await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, f"Email sent to {sender_email}.\nContent: {message}\n# --------------------------------------------")
    except Exception as e:
        print(f"Error: {e}")
        await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, f"Failed to send Email: {e}\n# --------------------------------------------")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("."))
    print("Bot started")
    await   sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, "Bot restarted at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


@client.event
async def on_member_join(member):
    print(member)
    await member.send("Hello, Please enter your college Email for verification.")
    await member.send("Example:")
    await member.send("https://i.imgur.com/L8aujqq.png")
    print(member.name, member, "Joined")

@client.event
async def on_message(message):
    if message.guild is None:
        if str(message.author.id) != '954317853228666930':
            msg = message.content
            if msg.lower().startswith("verify"):
                if not re.match(r"verify \w+\d+@gndec\.ac\.in", msg, re.IGNORECASE):
                    await message.reply("Wrong email specified. Kindly enter your GNDEC email. example: ABC1234@gndec.ac.in")
                else:
                    await message.reply("An OTP has been sent to your GNDEC email. Kindly copy paste it here.")
                    msg = msg.replace("verify ", "")
                    await send_otp(msg, message.author.id)
            if msg.startswith("gn1sd") and codes.get(f"{message.author.id}1") == msg:
                mail = codes.get(f"{message.author.id}2")
                nickName, rollnumber  = re.match(r'([a-zA-Z]+)(\d+)@gndec\.ac\.in', mail, re.IGNORECASE).groups()
                guild = client.get_guild(1123068128834899998)
                member = guild.get_member(message.author.id)
                try:
                    year = rollnumber[:2]
                    if(year == "20"):
                        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_FOURTH_YEAR))
                    elif(year == "21"):
                        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_THIRD_YEAR))
                    elif(year == "22"):
                        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_SECOND_YEAR))
                    elif(year == "23"):
                        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_FIRST_YEAR))
                    else:
                        await member.add_roles(discord.utils.get(guild.roles, id=1142771388504100864)) #default verified role if the above doesnt work
                    await member.edit(nick=nickName)
                    await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, f"user <@{message.author.id}> verified. \nName: {nickName}\nrollnumber:{rollnumber}\ndiscord ID: {message.author.id}\n# --------------------------------------------")
                    await message.reply("You are Verified!")
                except Exception as e:
                    print(f"Error during verification: {e}")
                    await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL,f"error during verification: {e}\n# --------------------------------------------")
                    await message.reply("There was an error during verification. Contact moderators for manual verification.")


async def send_otp(mail, id):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 10, 11, 12, 12, 13, 14, 15, 16, 17, 18, 19]
    otp = f"gn1sd{random.choice(letters)}{random.choice(letters)}{random.choice(numbers)}{random.choice(letters)}{random.choice(letters)}"
    codes[f"{id}1"] = otp
    codes[f"{id}2"] = mail
    await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, f'user <@{id}> (id: {id}) requesting verification.\n```email: {mail}\notp:{otp}```\n# ONLY GIVE IT IF YOU HAVE MANUALLY VERIFIED THE IDENTITY\n# --------------------------------------------')
    await sendEmail("amrinder2115012@gndec.ac.in", mail, "GNDEC Discord Verification OTP", otp)
    print('Email sent to ' + mail + " OTP: " + otp)

token = os.environ.get('GNDEC_BOT_TOKEN')
client.run(token)
