import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image, ImageDraw, ImageFont
import firebase_admin
from firebase_admin import credentials, firestore



cred = credentials.Certificate("./firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
event_name = 'cerebro'


docs = db.collection(event_name).stream()

def genCertificate(name,college,file_name):	
	image = Image.open('geek.png')
	font_type = ImageFont.truetype('TIMES.TTF', 128)
	draw = ImageDraw.Draw(image)
	draw.text(xy=(1500,1020),text=name,fill=(0,0,0),font=font_type)
	draw.text(xy=(500,1230),text=college,fill=(0,0,0),font=font_type)
	
	image.save(file_name)
	print('Certificate generated for =>'+ name)

def sendMail(email,file):
	print('Sending Mail to '+email)
	global event_name
	# reciever = email /// USE THE TO SEND MAIL TO CONCERNED PERSON FROM DATABASE
	reciever = "gauravv.ajay.boralkar@gmail.com"
	sender = "testcertificate211@gmail.com"

	msg = MIMEMultipart() 

	msg['From'] = sender
	msg['To'] = reciever

	msg['Subject'] = "Thanks for participating in PULZION 2019!"
	body = 'Congratulations for participating in '+event_name+' in PULZION 2019. Here is your participation Certificate.'

	msg.attach(MIMEText(body, 'plain'))

	filename = file
	attachment = open("./"+file, "rb")

	p = MIMEBase('application', 'octet-stream') 
	p.set_payload((attachment).read()) 
	encoders.encode_base64(p) 
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
	msg.attach(p) 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login(sender, "root@123") 
	text = msg.as_string() 
	s.sendmail(sender, reciever, text) 
	s.quit()
	
for doc in docs:
    data = doc.to_dict()
    user_email = data['email']
    user_name = data['name']
    user_college = data['college']
    file_name = user_name.replace(" ","") + '.png'
    genCertificate(user_name,user_college,file_name)
    sendMail(user_email,file_name)
    




