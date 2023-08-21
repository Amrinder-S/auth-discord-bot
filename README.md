# gndec-discord-bot
To set up the discord bot:

- first of all set up the enviornment variables. On windows use setx command.
```
set the SENDGRID_PASSWORD to your sendgrid API key
set the GNDEC_BOT_TOKEN to the discord bot token.
example:
setx SENDGRID_PASSWORD THIS_IS_SENDGRIND_PASSWORD
```
tip: NEVER PUSH HARDCODED PASSWORDS OR TOKENS THROUGH GITHUB.

- install python.
- now clone the repository using the command (learn how to use git from youtube)
```
git clone https://github.com/Amrinder-S/gndec-discord-bot/
```
- install the requirements. Cd into the folder and type 
```
pip install -r requirements.txt
```

- To run the bot type
```
python main.py
```
