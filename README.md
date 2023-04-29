![alt text](https://images.ctfassets.net/y6oq7udscnj8/5O3S2tFTAOuPtwnKWRvM6t/d003c6a5952d4387f5840db346acd25a/Mailgun-Validation__1_.png?w=1285&h=626&q=50&fm=png)

# Telegram Bot for Generating Reports from Fbtool and Keitaro trackers

This is a Python script that creates a Telegram bot using the aiogram library. The bot can generate three types of reports from the FBTool and Keitaro trackers: general information on advertising campaigns, daily conversions, and overall performance metrics.

Code uses the Selenium library to automate the process of logging into the fbtool.pro or keitaro website and navigating to the statistics page. First, it sets up the Chrome driver and loads some options for it, including the user agent, disabling the webdriver mode, and enabling headless mode. Then, it opens the fbtool.pro login page and loads any previously saved cookies, which are added to the browser session. After refreshing the page, it navigates to the statistics page, where the user can view their Facebook ad campaign statistics. Overall, the code automates the process of logging into fbtool.pro and accessing the statistics page, which can save time and effort for the user.


# Requirements

Before running the script, you will need to install the following libraries:

- aiogram
- numpy
- pandas
- selenium
- XlsxWriter

You will also need to have the Chrome browser installed on your machine, as the script uses the Selenium library to scrape data from the FBTool and Keitaro trackers.


# Usage

To use this script, you will need to create a Telegram bot and obtain its API token from the BotFather. You will also need to create a config.ini file with the following contents:

```
[TELEGRAM]
token = YOUR_TELEGRAM_BOT_API_TOKEN

[FBTOOL]
username = YOUR_EMAIL
password = YOUR_PASSWORD

[KEITARO]
username = YOUR_FACEBOOK_EMAIL
password = YOUR_PASSWORD
```


Replace the placeholders with your own information.

Once you have created the config.ini file and installed the required libraries, you can run the script:

```
python telegram_bot.py
```

The script will start the Telegram bot. Users can send the bot commands to generate reports from the FBTool and Keitaro trackers.

