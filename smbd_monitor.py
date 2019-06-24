import os
import smtplib, ssl
from email.message import EmailMessage
import subprocess

# grab status of samba server from last in log
def samba_state():
    samba_status = subprocess.check_output(['service', 'smbd', 'status'])
    samba_status = str(samba_status.splitlines()[-1])
    return samba_status.find('Started')


# if running, exit script
if samba_state() != -1:
    quit()

# else restart up to five times unless unsucessful
else:

    for i in range(1, 5):
        subprocess.check_output(['service', 'smbd', 'status'])

        if samba_state() == -1:
            quit()

    # else email to prompt fix
    ############# need to check if email has been recently sent or problem fixed
    sender_email = os.environ.get('SMBD_MONITOR_SEND_EMAIL')
    sender_password = os.environ.get('SMBD_MONITOR_SEND_PASSWORD')
    receiver_email = os.environ.get('SMBD_MONITOR_RECEIVE_EMAIL')

    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, sender_password)
        msg = EmailMessage()
        msg.set_content('')
        msg['Subject'] = 'Server down: Samba'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        server.sendmail(sender_email, receiver_email, msg)
