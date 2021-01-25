# telegram_bot
Project Overview : 
 
   I have created app_monitoring_bot.py to monitor status of my applications running on remote server one on windows and another on Linux Server. This Programs checks the running status and monitors the output of application if any of application crashed or any exception occurs or if it observe any change in output this will notify me on my telegram's group.
   
Configuration instructions :

  To run this program we need to have python installed on our system. Telegram account, and a bot. 
  
  Bots are third-party applications that run inside Telegram. To communicate with Telegram API we are going to use python library called telepot.

        pip install teletpot
  
  we need the token to acces HTTP API and chat_id of the group in which we added our bot and also we can add our team members to whom we wants to share the status.
  
  Initially a new Bot can only read messages that starts with a '/' to let it read all message we need to change can_read_all_group_messages to False

     PrivacyMode of a Bot :
      'Enable' - your bot will only receive messages that either start with the '/' symbol or mention the bot by username.
      'Disable' - your bot will receive all messages that people send to groups.

    To do so : 

      Go to BotFather and change privacy setting for Bot
        /setprivacy
      and select your bot for which you want to change the settings
      change the status to disable.
      Then check for status of can_read_all_group_messages which turns to True
