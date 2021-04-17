
import smtplib 
from email.message import EmailMessage

import threading
import time

import requests
import json



# Config info

EmailAdd = "moneyalert.rasp@gmail.com" #senders Gmail id over here
Pass = "" #senders Gmail's Password over here 

URL='https://api.wazirx.com/api/v2/tickers/' # URL + name

def Sendmail(To,subject,body):
    msg = EmailMessage()
    msg['Subject'] = subject # Subject of Email
    msg['From'] = EmailAdd
    msg['To'] = To # Reciver of the Mail
    msg.set_content(body) # Email body or Content

    #### >> Code from here will send the message << ####
    
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: #Added Gmails SMTP Server
        smtp.login(EmailAdd,Pass) #This command Login SMTP Library using your GMAIL
        smtp.send_message(msg) #This Sends the message


# API call Here

alerts=[
    {
        'coin':'btcinr',
        'price':50_00_000,
        'direction':1 ,  # 1 = up 0 = Down
        'email':'moneyalert.rasp@gmail.com' ,
        },
    {   
        'coin':'ltcinr',
        'price':30_515,
        'direction':1 ,  # 1 = up 0 = Down
        'email':'moneyalert.rasp@gmail.com' ,
        }
        ]

def api_thread():
    while True:
        time.sleep(1)
        for alert in alerts:
            coin=alert['coin']
            To=alert['email']
            subject=f'This is a price alert to {To} for {coin}'
            
            r = requests.get(URL+coin)
            j=r.json()
            
            curr_price=int(float(j['ticker']['sell']))

            
            
            if not alert['direction'] and curr_price<alert['price']:
                body=f" Hey The price of {coin} is now less than {alert['price']}"
                Sendmail(To,subject,body)
                alerts.remove(alert)
            elif alert['direction'] and curr_price>alert['price']:
                body=f" Hey The price of {coin} is now greater than {alert['price']}"
                Sendmail(To,subject,body)
                alerts.remove(alert)

def input_thread():
    while True:
        coin=input("Enter the Coin name and Base currency For Ex. btcinr,ltcinr,xeminr : \n")
        price=int(input("Set the alert at :  \n"))
        direction=int(input("0 for lower limit : 1 for upper limit \n"))
        email=input("Enter your email id : \n")
        print("Creating alert")
        
        new_alert={}
        new_alert['coin']=coin
        new_alert['price']=price
        new_alert['direction']=direction
        new_alert['email']=email

        alerts.append(new_alert)

        print(f"Alert created you will be notified at {email}")



# Start parallel threads for input and api

t1=threading.Thread(target=api_thread,args=())
t2=threading.Thread(target=input_thread,args=())
t1.start()
t2.start()
t1.join()
t2.join()




    
