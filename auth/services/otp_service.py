import os
import secrets
import smtplib
import traceback
from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# from variable_service import SMTP_SERVER,serverpassword,serverusername
SMTP_SERVER= os.getenv("SMTP_SERVER") #"email-smtp.eu-central-1.amazonaws.com"
serverusername=  os.getenv("serverusername")#"AKIARZL4X6FTMDTXXRYI"
serverpassword= os.getenv("serverpassword") #"BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"
    

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")


def generate_resend_token():
    return secrets.token_urlsafe(32)

def send_otp_via_email(email: str, otp: str):
    msg = MIMEMultipart()
    msg['From'] = "aisha.rana@codelabs.inc"
    msg['To'] = email
    msg['Subject'] = "Your OTP Code"
    # Get the directory of the current file (auth.py)
    current_dir = os.path.dirname(__file__)

    # Move up two levels to the 'auth' directory
    auth_dir = os.path.dirname(current_dir)

    # Define the paths to the 'templates' and 'images' directories
    html_template_path = os.path.join(auth_dir, 'templates', 'otp.html')
    images_dir = os.path.join(auth_dir, 'templates', 'images', 'otp')
    print(current_dir)
    print(images_dir)
    print(html_template_path)
    # current_dir = os.path.dirname(__file__)
    # html_template_path = os.path.join(current_dir, 'templates', 'otp.html')
    # images_dir = os.path.join(current_dir, 'images', 'otp')
    # print("0")
    try:
        with open(html_template_path, 'r') as file:
            html_template = file.read()
        
        # Insert the OTP code into the HTML template
        html_content = html_template.replace("OTP", otp)
        # print("1")
         # Find and embed images
        embedded_images = []
        for image_name in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_name)
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', f'<{image_name}>')
                msg.attach(image)
                embedded_images.append(image_name)
        
        # Replace image src in HTML content with cid
        for image_name in embedded_images:
            html_content = html_content.replace(f'/images/{image_name}', f'cid:{image_name}')        

        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(serverusername, serverpassword)
        text = msg.as_string()
        server.sendmail("aisha.rana@codelabs.inc", email, text)
        server.quit()
        print(f"OTP {otp} sent to {email}")
        message="OTP Sent successfully"
        return message
    except Exception as e:
        traceback.print_exc()
        print(f"Failed to send OTP: {e}")
        message="Failed to send OTP"
        return message

def send_otp_via_sms(phone_number: str, otp: str):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your OTP code is: {otp}",
        from_="<Twilio Verified Number>",
        to=phone_number, # Should also be Twilio verified for trial account
    )

    print(message.body)