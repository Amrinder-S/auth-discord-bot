import discord
import random
import re
import os
import smtplib
from datetime import datetime
import datafunction as mydb
from discord import app_commands
# todo : you have to check if the person is in the server first before setting roles.

if os.name == 'nt':
    os.system("cls")
else:
    os.system("clear")

#global variables
GNDEC_DISCORD_ID = 1123068128834899998
GNDEC_LOGS_CHANNEL = 1142833474185744465
ROLE_FIRST_YEAR = 1123938097957191810
ROLE_SECOND_YEAR = 1123938146141347860
ROLE_THIRD_YEAR = 1124275055749251092
ROLE_FOURTH_YEAR = 1124275287648112700
mail_pattern = r"^[a-zA-Z]+20\d+@gndec.ac.in$|^[a-zA-Z]+21\d+@gndec.ac.in$|^[a-zA-Z]+22\d+@gndec.ac.in$|^[a-zA-Z]+_23\d+@gndec.ac.in$|^[a-zA-Z]+_[a-zA-Z]+23\d+@gndec.ac.in$"
normal_mail_pattern = r"^[a-zA-Z]+20\d+@gndec.ac.in$|^[a-zA-Z]+21\d+@gndec.ac.in$|^[a-zA-Z]+22\d+@gndec.ac.in$"
new_mail_pattern = r"^[a-zA-Z]+_23\d+@gndec.ac.in$"
alt_mail_pattern = r"^[a-zA-Z]+_[a-zA-Z]+23\d+@gndec.ac.in$"

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

#------------------- Slash Commands go here.
tree = app_commands.CommandTree(client)
def checkEmail(v):
    if not re.fullmatch(mail_pattern, v, re.IGNORECASE):
        return True
    else:
        return False
@tree.command(name = "getunverified", description = "used to get members who are sent the OTP but have not verified yet..",guild=discord.Object(id=GNDEC_DISCORD_ID))
async def getUnverified(interaction):
    await interaction.response.send_message("getting unverified users.", ephemeral=False)
    wrongFormat = "Wrong Format:"
    unknownReason = "Unknown Reason:"
    unverified_otp = mydb.getAllOtp()
    for i in unverified_otp:
        if(checkEmail(i.email)):
            wrongFormat = f"{wrongFormat}\n<@{i.id}>"
        else:
            unknownReason = f"{unknownReason}\n<@{i.id}>"
    await interaction.followup.send(f"### Wrong format\n```{wrongFormat}```", ephemeral=False)
    await interaction.followup.send(f"### Unknown reason\n```{unknownReason}```", ephemeral=False)
        

@tree.command(name = "syncroles", description = "used to synchronize all roles again.",guild=discord.Object(id=GNDEC_DISCORD_ID))
async def syncRolesCommand(interaction):
    await interaction.response.send_message("Syncing.", ephemeral=True)
    await interaction.followup.send(str(await syncRoles()), ephemeral=True)

@tree.command(name = "removestudent", description = "used to remove a student from verifiied status",guild=discord.Object(id=GNDEC_DISCORD_ID))
async def removeStudentCommand(interaction: discord.Interaction, member: discord.Member):
    """removes the student from verified status.

    Parameters
    -----------
    member: discord.Member
        the member to remove from verified status
    """
    await interaction.response.send_message(f"Removing {member.name}", ephemeral=True)
    if(mydb.removeStudent(member.id)):
        await interaction.followup.send(f"Member {member.name} removed.", ephemeral=True)
    else:
        await interaction.followup.send(f"Failed to remove member {member.name}.", ephemeral=True)
        
@tree.command(name = "removeotp", description = "used to reset a student's otp",guild=discord.Object(id=GNDEC_DISCORD_ID))
async def removeotp(interaction: discord.Interaction, member: discord.Member):
    """removes the student from otp status.

    Parameters
    -----------
    member: discord.Member
        the member to reset otp for.
    """
    await interaction.response.send_message(f"Removing {member.name}", ephemeral=True)
    if(mydb.removeOtp(member.id)):
        await interaction.followup.send(f"Member {member.name} removed.", ephemeral=True)
    else:
        await interaction.followup.send(f"Failed to remove member {member.name}.", ephemeral=True)


@tree.command(name = "getstudent", description = "used to get the student's information.",guild=discord.Object(id=GNDEC_DISCORD_ID))
async def removeotp(interaction: discord.Interaction, member: discord.Member):
    """gets the student's information.

    Parameters
    -----------
    member: discord.Member
        the member to get information of.
    """
    await interaction.response.send_message(f"getting information of {member.name}", ephemeral=True)
    info = mydb.getStudent(member.id)
    if(info):
        await interaction.followup.send(f"Member {member.name}, {info.roll_number}, {info.name}.", ephemeral=True)
    else:
        await interaction.followup.send(f"User is not verified.", ephemeral=True)


#------------------- Client events (on member join, on ready, on message etc.)
@client.event
async def on_ready():
#    await client.change_presence(activity=discord.Game("."))
    print("Bot started")
    #await   sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, "Bot restarted at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    await tree.sync(guild=discord.Object(id=GNDEC_DISCORD_ID))

@client.event
async def on_member_join(member):
    # await member.send("Hello, Welcome to GNDEC discord")
    student = mydb.getStudent(member.id)
    if student:
        await addRoleForVerifiedUser(member, student)
    print(member, "Joined")

@client.event
async def on_message(message):
    if message.guild is None:
        if str(message.author.id) != '954317853228666930':
            msg = message.content
            if '@' in msg:
                if not re.fullmatch(mail_pattern, msg, re.IGNORECASE):
                    await message.reply("External email unsupported. Kindly enter your GNDEC email.\n If you are in 1st year, your email should be formatted like this: firstname_rollnumber@gndec.ac.in")
                else:
                    try:
                        await send_otp(msg, message.author.id)
                    except:
                        await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL,f"Errot while sending OTP to user <@{message.author.id}, {e}>\n# --------------------------------------------")
                        await message.reply("There was an error while sending OTP. contact an admin for manual verification")
            
            if msg.startswith("gn1sd") and mydb.checkOtp(message.author.id, msg):
                mail = mydb.getEmailForOtp(message.author.id)
                if re.fullmatch(new_mail_pattern, mail, re.IGNORECASE):
                    nickName, rollnumber  = re.match(r'([a-zA-Z]+)_(\d+)@gndec\.ac\.in', mail, re.IGNORECASE).groups()
                elif re.fullmatch(alt_mail_pattern, mail, re.IGNORECASE):
                    nickName, rollnumber  = re.match(r'([a-zA-Z]+_[a-zA-Z]+)(23\d+)@gndec\.ac\.in', mail, re.IGNORECASE).groups()
                elif re.fullmatch(normal_mail_pattern, mail, re.IGNORECASE):
                    nickName, rollnumber = re.match(r"([a-zA-Z]+)(\d+)@gndec.ac.in", mail, re.IGNORECASE).groups()
                else:
                    nickName = "unknown"
                    rollnumber = mail
                guild = client.get_guild(GNDEC_DISCORD_ID)
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
                    try:
                        if (nickName != "unknown"):
                            await member.edit(nick=str(nickName).capitalize())
                    except Exception as e:
                        await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, f"There was an error while changing nickname of {message.author.name}, user probably has higher role than the bot.\n# --------------------------------------------")
                    await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, f"user <@{message.author.id}> verified. \nName: {nickName}\nrollnumber:{rollnumber}\ndiscord ID: {message.author.id}\n# --------------------------------------------")
                    mydb.addStudent(message.author.id, nickName, year, rollnumber)
                    mydb.removeOtp(message.author.id)
                    await message.reply("You are Verified!")
                except Exception as e:
                    print(f"Error during verification: {e}")
                    await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL,f"error during verification: {e}\n# --------------------------------------------")
                    await message.reply("There was an error during verification. Contact moderators for manual verification.")



#------------------- Functions definitions.
async def send_otp(mail, id):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y", "z"]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 10, 11, 12, 12, 13, 14, 15, 16, 17, 18, 19]
    otp = f"gn1sd{random.choice(letters)}{random.choice(letters)}{random.choice(numbers)}{random.choice(letters)}{random.choice(letters)}"
    guild = client.get_guild(GNDEC_DISCORD_ID)
    member = guild.get_member(id)
    if not mydb.getStudent(id):
        if not mydb.checkOtpByEmail(mail) and not mydb.checkOtpByUser(id): #checking by email to avoid sending multiple emails. checking by id to avoid single user sending multiple verification requests from multiple emails.
            mydb.addOtp(id, mail, otp)
            await member.send("An OTP has been sent to your GNDEC email. Kindly copy paste it here.")
            await sendMessage(GNDEC_DISCORD_ID, GNDEC_LOGS_CHANNEL, f'user <@{id}> (id: {id}) requesting verification.\n```email: {mail}\notp:{otp}```\n# ONLY GIVE IT IF YOU HAVE MANUALLY VERIFIED THE IDENTITY\n# --------------------------------------------')
            await sendEmail("aps_phy@gndec.ac.in", mail, "GNDEC Discord Verification OTP", otp) # todo
        else:
            await member.send("Wait atleast 5 minutes for email to arrive.\nOtherwise message a moderator if it doesn't arrive after 5 minutes.")
    else:
        await member.send(f"You are already verified with roll number: {mydb.getStudent(id).roll_number}")

async def syncRoles():
    students = mydb.getAll()
    syncedCount = 0
    for student in students:
        guild = client.get_guild(GNDEC_DISCORD_ID)
        member = guild.get_member(student.id)
        if(student.batch == 20):
            await member.add_roles(discord.utils.get(guild.roles,id=ROLE_FOURTH_YEAR))
        elif(student.batch == 21):
            await member.add_roles(discord.utils.get(guild.roles,id=ROLE_THIRD_YEAR))
        elif(student.batch == 22):
            await member.add_roles(discord.utils.get(guild.roles,id=ROLE_SECOND_YEAR))
        elif(student.batch == 23):
            await member.add_roles(discord.utils.get(guild.roles,id=ROLE_FIRST_YEAR))
        else:
            await member.add_roles(discord.utils.get(guild.roles, id=1142771388504100864)) #default verified role if the above doesnt work
        if(member.top_role.position < guild.me.top_role.position):
            await member.edit(nick=str(student.name).capitalize())
            syncedCount = syncedCount + 1
        else:
            print(f"[Warning] unable to change nickname of {student.name}, user probably has higher role than the bot. id: <@{student.id}>\n# --------------------------------------------")
    return f"Synced {syncedCount} members successfully!"

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

async def addRoleForVerifiedUser(member, student):
    guild = client.get_guild(GNDEC_DISCORD_ID)
    if(str(student.batch) == "20"):
        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_FOURTH_YEAR))
    elif(str(student.batch) == "21"):
        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_THIRD_YEAR))
    elif(str(student.batch) == "22"):
        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_SECOND_YEAR))
    elif(str(student.batch) == "23"):
        await member.add_roles(discord.utils.get(guild.roles,id=ROLE_FIRST_YEAR))
    else:
        await member.add_roles(discord.utils.get(guild.roles, id=1142771388504100864)) #default verified role if the above doesnt work
    await member.edit(nick=str(student.name).capitalize())
#------------------- error handling

@client.event
async def on_disconnect():
    print("Disconnected from Discord")

@client.event
async def on_error(event, *args, **kwargs):
    # Handle errors here
    pass


#------------------- running the client.
try:
    token = os.environ.get('GNDEC_BOT_TOKEN')
    client.run(token)
except Exception as e:
    print(f"{e}")



