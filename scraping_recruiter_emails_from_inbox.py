import pandas as pd
import pyzmail
import imapclient

###Setting up connection to gmail and reading all emails
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login('mehdi.******@gmail.com', 'password')
imapObj.select_folder('INBOX', readonly=True)

###Searching for mail by subject keywords.Each mail is then given an ID 
UIDs = imapObj.search(['OR','OR','OR','OR','OR','OR','OR','OR','OR','SUBJECT','data','SUBJECT','science','SUBJECT','analyst','SUBJECT','sql','SUBJECT','recruiting','SUBJECT','career','SUBJECT','job','SUBJECT','phone','SUBJECT','analytics','SUBJECT','opening'])  
sender_email_list=[]
sender_name_list=[]

###Looping through relevant mails and extracting email address and first name
for i in UIDs:
 rawMessages = imapObj.fetch([i], ['BODY[]', 'FLAGS'])
 message = pyzmail.PyzMessage.factory(rawMessages[i][b'BODY[]'])
 sender_details=message.get_addresses('from')
 #Extracting email
 sender_email=sender_details[0][1]
 #Extracting first name
 sender_name =sender_details[0][0].split()[0] 
 #Adding to list
 sender_email_list=sender_email_list+[sender_email]
 sender_name_list =sender_name_list +[sender_name]

###Joining email and name columns and exporting as csv for editing
list_subject=pd.DataFrame(list(zip(sender_email_list,sender_name_list)))
list_subject.to_csv('email_name_list.csv',index=False)

import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.connect('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login('mehdi.******@gmail.com', 'password')

###Reading edited list of emails and first names
list_subject=pd.read_csv('list_subject.csv')

###Looping through list and sending email
for i in range(0,len(list_subject)):
  message = 'Subject: {}\n\n{}'.format('Reconnecting..', 'Hi %s,\nWe were in touch regarding some openings a while back. Just wanted to let you know I am available currently and came across some great roles which I would be interested in discussing.\nRegards,\nMehdi Mujtaba' %list_subject.iloc[i][1])
  server.sendmail('mehdi.******@gmail.com', '%s' %list_subject.iloc[i][0] ,message)
