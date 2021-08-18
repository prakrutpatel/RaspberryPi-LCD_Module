import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime

# Change to your own account information
# Account Information
to = '******' # Email to send to.
gmail_user = '******' # Email to send from. (MUST BE GMAIL)
gmail_password = '*******' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='hostname -I'  # Linux command to retrieve ip address.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()  # Get data from 'p terminal'.
data = data[0].decode('UTF-8')

# Creates a sentence for each ip address.
my_ip_a = 'Your Pi3 IP is %s' % data

# Creates the text, subject, 'from', and 'to' of the message.
msg = MIMEText(my_ip_a)
msg['Subject'] = 'IP For RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
# Sends the message
smtpserver.sendmail(gmail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()
