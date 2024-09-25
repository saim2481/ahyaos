import os
import smtplib
from datetime import timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from twilio.rest import Client
from dotenv import load_dotenv

# from variable_service import SMTP_SERVER,serverpassword,serverusername
load_dotenv()


SMTP_SERVER= os.getenv("SMTP_SERVER") #"email-smtp.eu-central-1.amazonaws.com"
serverusername=  os.getenv("serverusername")#"AKIARZL4X6FTMDTXXRYI"
serverpassword= os.getenv("serverpassword") #"BJXnGzShMJZ+xZFfefaaQlcBBHNoZ+IhrOrr/YRBf8O3"
   


def send_reset_password_email(email: str, token: str):
    msg = MIMEMultipart()
    msg['From'] = "aisha.rana@codelabs.inc"
    msg['To'] = email
    msg['Subject'] = "Reset your Password"

    # Get the directory of the current file (auth.py)
    current_dir = os.path.dirname(__file__)


    # Move up two levels to the 'auth' directory
    auth_dir = os.path.dirname(os.path.dirname(current_dir))

    # Define the paths to the 'templates' and 'images' directories
    html_template_path = os.path.join(auth_dir, 'templates', 'new-password.html')
    images_dir = os.path.join(auth_dir, 'templates', 'images', 'reset_password')

    try:
        with open(html_template_path, 'r') as file:
            html_template = file.read()
        
        reset_link = f"http://your-frontend-url/reset-password?token={token}"

        html_content = html_template.replace("URL", reset_link)

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
        return True
    
    except Exception as e:
        print(f"Failed to send Reset Password Link: {e}")
        return False
    
def send_approval_email(email: str):
    msg = MIMEMultipart()
    msg['From'] = "aisha.rana@codelabs.inc"
    msg['To'] = email
    msg['Subject'] = "Account Approved"

    # Path to the HTML template
    # html_template_path = os.path.join(r"C:\Users\Aisha Rana\Downloads\auth\auth\templates", 'new-email.html')
    # images_dir = os.path.join(r"C:\Users\Aisha Rana\Downloads\auth\auth\templates", 'images')
    html_template_path = os.path.join(r"auth\templates", 'new-email.html')
	# html_template_path = os.path.join(current_dir, 'otp.html')
    images_dir = os.path.join(r"auth\templates", 'images','otp')
    try:
        with open(html_template_path, 'r') as file:
            html_template = file.read()
        
        html_content = html_template
        
        # Embed images
        embedded_images = {}
        for image_name in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_name)
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', f'<{image_name}>')
                msg.attach(image)
                embedded_images[image_name] = image_name
        
        # Replace image src in HTML content with cid
        for image_name, cid_name in embedded_images.items():
            html_content = html_content.replace(f'src="images/{image_name}"', f'src="cid:{cid_name}"')
        
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(serverusername, serverpassword)
        text = msg.as_string()
        server.sendmail("aisha.rana@codelabs.inc", email, text)
        server.quit()
        print(f"Approval email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send approval email: {e}")
        return False
    





def send_rejection_email(email: str) -> bool:
    msg = MIMEMultipart()
    msg['From'] = "aisha.rana@codelabs.inc"
    msg['To'] = email
    msg['Subject'] = "Account Rejected"

    # Path to the HTML template
    html_template_path = os.path.join(r"auth\templates", 'rejected.html')
    images_dir = os.path.join(r"auth\templates", 'images','otp')

    try:
        with open(html_template_path, 'r') as file:
            html_template = file.read()
        
        html_content = html_template
        
        # Embed images
        embedded_images = {}
        for image_name in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_name)
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', f'<{image_name}>')
                msg.attach(image)
                embedded_images[image_name] = image_name
        
        # Replace image src in HTML content with cid
        for image_name, cid_name in embedded_images.items():
            html_content = html_content.replace(f'src="images/{image_name}"', f'src="cid:{cid_name}"')
        
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(serverusername, serverpassword)
        text = msg.as_string()
        server.sendmail("aisha.rana@codelabs.inc", email, text)
        server.quit()
        print(f"Rejection email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send rejection email: {e}")
        return False
    

    



def send_profile_verified_email(email: str):
    msg = MIMEMultipart()
    msg['From'] = "aisha.rana@codelabs.inc"
    msg['To'] = email
    msg['Subject'] = "Profile Verified"

    # Path to the HTML template
    html_template_path = os.path.join("auth", "templates", 'verified.html')
    images_dir = os.path.join("auth", "templates", 'images','otp')

    try:
        with open(html_template_path, 'r') as file:
            html_template = file.read()
        
        html_content = html_template
        
        # Embed images
        embedded_images = {}
        for image_name in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_name)
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', f'<{image_name}>')
                msg.attach(image)
                embedded_images[image_name] = image_name
        
        # Replace image src in HTML content with cid
        for image_name, cid_name in embedded_images.items():
            html_content = html_content.replace(f'src="images/{image_name}"', f'src="cid:{cid_name}"')
        
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(serverusername, serverpassword)
        text = msg.as_string()
        server.sendmail("aisha.rana@codelabs.inc", email, text)
        server.quit()
        print(f"Verification email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        return False


# Utility function to create reset token






def send_profile_not_accepted_email(email: str):
    msg = MIMEMultipart()
    msg['From'] = "aisha.rana@codelabs.inc"
    msg['To'] = email
    msg['Subject'] = "Profile Not Accepted"

    # Path to the HTML template
    html_template_path = os.path.join("auth", "templates", 'unapproved.html')
    images_dir = os.path.join("auth", "templates", 'images','otp')

    try:
        with open(html_template_path, 'r') as file:
            html_template = file.read()
        
        html_content = html_template
        
        # Embed images
        embedded_images = {}
        for image_name in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_name)
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', f'<{image_name}>')
                msg.attach(image)
                embedded_images[image_name] = image_name
        
        # Replace image src in HTML content with cid
        for image_name, cid_name in embedded_images.items():
            html_content = html_content.replace(f'src="images/{image_name}"', f'src="cid:{cid_name}"')
        
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(serverusername, serverpassword)
        text = msg.as_string()
        server.sendmail("aisha.rana@codelabs.inc", email, text)
        server.quit()
        print(f"Profile not accepted email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send profile not accepted email: {e}")
        return False





def send_profile_under_verification_email(email: str, ):
    msg = MIMEMultipart()
    msg['From'] = "aisha.rana@codelabs.inc"
    msg['To'] = email
    msg['Subject'] = "Profile Under Verification"

    html_template_path = os.path.join("auth", "templates", 'underReview.html')
    images_dir = os.path.join("auth", "templates", 'images','otp')

    try:
        with open(html_template_path, 'r') as file:
            html_template = file.read()
        
        html_content = html_template
        
        embedded_images = {}
        for image_name in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_name)
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                image = MIMEImage(img_data)
                image.add_header('Content-ID', f'<{image_name}>')
                msg.attach(image)
                embedded_images[image_name] = image_name
        
        for image_name, cid_name in embedded_images.items():
            html_content = html_content.replace(f'src="images/{image_name}"', f'src="cid:{cid_name}"')
        
        msg.attach(MIMEText(html_content, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()
        server.login(serverusername, serverpassword)
        text = msg.as_string()
        server.sendmail("aisha.rana@codelabs.inc", email, text)
        server.quit()
        print(f"Profile under verification email sent to {email}")
        return True
    except Exception as e:
        print(f"Failed to send profile under verification email: {e}")
        return False
