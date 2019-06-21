import os
import smtplib, ssl
import subprocess

# grab status of samba server from last in log
smbstatus = subprocess.check_output(['service', 'smbd', 'status'])
smbstatus = smbstatus.split('\n')[-2]
state = smbstatus.find('Started', beg=0, end=len(string))

# if found
if state != -1:
    quit()

# else
sender_email = os.environ.get('SMBD_MONITOR_SEND_EMAIL')
sender_password = os.environ.get('SMBD_MONITOR_SEND_PASSWORD')
receiver_email = os.environ.get('SMBD_MONITOR_RECEIVE_EMAIL')

port = 465
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, sender_password)
    # TODO: Send email here
