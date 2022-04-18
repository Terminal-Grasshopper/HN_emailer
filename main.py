import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()
content_placeholder = ''


def extract_news(url):
    print('Extracting...')
    cnt = ''
    cnt += ('Hacker News top stories:\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup= BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.findAll('td', attrs={'class':'title', 'valign':''})):
        cnt+=((str(i+1)+' :: '+tag.text+'\n'+'<br>') if tag.text!='More' else '')
    return(cnt)



cnt = extract_news('https://news.ycombinator.com/')
content_placeholder += cnt
content_placeholder += '<br>--------<br>'
content_placeholder += '<br><br>End of message'


print('Composing email...')

server = 'smtp.gmail.com'
port = 587
sender = '***'
password = '***'
receiver = '***'

msg = MIMEMultipart()

msg['Subject']='Top HN Stories [Automated]'+' ' + str(now.day) + str(now.month) + str(now.year)
msg['To'] = sender
msg['From'] = receiver

msg.attach(MIMEText(content_placeholder, 'html'))

print('Initiating server...')
server=smtplib.SMTP(server, port)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(sender, password)
server.sendmail(sender, receiver, msg.as_string())

print('Email sent...')
server.quit()




