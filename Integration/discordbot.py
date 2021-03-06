import discord
import urllib.parse
import logging
import time
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

#Here's the pip for this!
#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

#Speadsheet URL will be in GDrive
#Make sure you grab your corresponding key off the gdrive and download it onto PATH, and then rename to "key.json". If you open the key, you should see all the authorized accounts you need. 
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SERVICE_ACCOUNT_FILE = ('key.json')
# creds = None
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# spreadsheetURL = 'URL'
# service = build('sheets', 'v4', credentials=creds)
def logon():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)  
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

client = discord.Client()
start = time.time()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    googleDrive = urllib.parse.quote('drive.google.com/drive/u/0/folders/1CCP-LOptbYmCFPcCLKkbacRMxh7sKZaW')
    GitHub = urllib.parse.quote('github.com/echavemann/nuft')
    helpsheet = urllib.parse.quote('docs.google.com/spreadsheets/d/1Xwrkx1DEE_78wCpW5xocmMp4NK1n5utN7murCc9ywJE')
    if message.author == client.user:
        return

    if message.content.startswith('$ping'):
        end = time.time()
        uptime = end-start
        uptime = uptime // 1
        uptime = str(uptime)
        await message.channel.send('pong! Bot Uptime: ' + uptime + ' seconds')
        
    if message.content.startswith('$ethan'):
        await message.channel.send('instagram.com/echavemann')

    if message.content.startswith('$drive'):
        await message.channel.send('https://' + googleDrive)

    if message.content.startswith('$github'):
        await message.channel.send('https://' + GitHub)

    if message.content.startswith('$status'):
        await message.channel.send('System Uptime:' + '0 hours, 0 minutes, 0 seconds.')

    if message.content.startswith('$next'):
        await message.channel.send('Ping ethan lmao')

    if message.content.startswith('$last'):
        await message.channel.send('https://' + 'docs.google.com/document/d/1S7JFwrTACRTkfaJqQ69xDT9jvn1R2GqJDikouw7MBoc/edit')

    if message.content.startswith('$roster'):
        await message.channel.send('https://' + 'docs.google.com/spreadsheets/d/1yZILT3q-o7nBSn2yBpMWeaJIS8FeTAxmjZIFapTIe74/edit#gid=0')

    if message.content.startswith('$form'):
        await message.channel.send('https://' + 'docs.google.com/forms/d/e/1FAIpQLSf78oBbq1z7UhUlqBWh8qemwc2fWpiKUMMegWdqYM7AIr6xSg/alreadyresponded')
    
    if message.content.startswith('$project'):
        await message.channel.send('https://' + 'github.com/users/echavemann/projects/3/views/1')

    if message.content.startswith('$help'):
        await message.channel.send('https://' + helpsheet)

client.run('')
