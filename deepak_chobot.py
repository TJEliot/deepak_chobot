from bs4 import BeautifulSoup

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import praw
import time
import re
import requests
import bs4
import os 
path = '/home/pi/deepak_chobot/commented.txt'

def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit(client_id='hNjqvmwFwdlc_A', client_secret='kpZ3Xb512WMgtiCG3aetBUnqVv0', user_agent='deepak chopra', username='Deepak_Chopra', password='soundsdeepman')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def fetchdata(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    tag = soup.find('h2')
    data = ''
    data = tag.text
    length = len(data) - 3
    data = data[1:length]
    print(data)
    return data

def run_chobot(reddit):
    print("Getting 250 comments...\n")

    for comment in reddit.subreddit('atheism').comments(limit=250):
        match = re.findall(r"(?i)[a-z]*[A-Z]*[0-9]*quantum|(?i)[a-z]*[A-Z]*[0-9]*chopra|(?i)[a-z]*[A-Z]*[0-9]*mystic|(?i)[a-z]*[A-Z]*[0-9]*magic", comment.body)
        if match:
            print("Deepak was mentioned in comment ID:" + comment.id)
            myurl='http://wisdomofchopra.com/iframe.php'

            file_obj_r=open(path, 'r')

            try:
                print("trying to scrape")
                explanation=fetchdata(myurl)
#                explanation = "test"
            except:
                print("Exception!! possibly fucked up url")
                break
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print('comment is unique...posting reply\n')
                    comment.reply(explanation)

                    file_obj_r.close()

                    file_obj_w = open(path, 'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already replied')

            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)

def main():
    reddit = authenticate()
    while True:
        run_chobot(reddit)

if __name__ == '__main__':
    main()
