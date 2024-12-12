# http requests
import requests
# web scraping
from bs4 import BeautifulSoup
# send email
from smtplib import SMTP
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time
import datetime


# global
URL = "https://news.ycombinator.com/" # website
SERVER = 'smtp.gmail.com' # smtp server
PORT = 587  # port number
FROM = '' # sender email address
PASS = '' # sender password
TO = '' # receivers email addresses


def get_soup():
    # get webpage content
    response = requests.get(URL)
    content = response.content
    # parse content
    soup = BeautifulSoup(content, 'html.parser')
    
    return soup


def extract_news():
    print("Extracting news...")
    soup = get_soup()

    # find all titles
    content = ''
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign':''})):
        content += (str(i+1) + ' :: ' + tag.text + '\n' + '<br>') if tag.text != "More" else ''

    return content


def build_msg(content):
    print('Building msg...')
    now = datetime.datetime.now()

    msg = MIMEMultipart()
    msg['Subject'] = 'Top Hacker News Stories [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
    msg['From'] = FROM
    msg['To'] = TO
    msg.attach(MIMEText(content, 'html'))

    return msg


def send_email(content):
    msg = build_msg(content)

    print('Initiating server...')
    server = SMTP(SERVER, PORT)
    server.starttls()
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    print('Email sent...')
    server.quit


def main():
    content = extract_news()
    send_email(content)


if __name__ == "__main__":
    main()
