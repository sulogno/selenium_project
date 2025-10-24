import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask


YOUR_EMAIL = "rhitsarkar@gmail.com"      # Your email address
YOUR_APP_PASSWORD = "gppgle app password" # Your Google App Password
YOUR_NAME = "Sulogno Sarkar"

# --- RECIPIENT & SUBJECT ---
TO_EMAIL = "tech@themedius.ai"
CC_EMAIL = "hr@themedius.ai"
SUBJECT = f"Python (Selenium) Assignment - {YOUR_NAME}"

# --- ATTACHMENT ---
SCREENSHOT_FILE = "confirmation.png" # Must match the file from fill_form.py

app = Flask(__name__)

def create_email_body():
    """Creates the HTML content for the email."""
    
    # --- YOUR SUBMISSION LINKS (Fill these in) ---
    github_link = "https://github.com/sulogno/selenium_project"
    resume_link = "https://drive.google.com/file/d/1ufgqTy6CHEXa4oWHM3ezrGo0F3P50WSw/view?usp=drive_link" # e.g., Google Drive or portfolio link
    projects_link = "https://sulogno-sarkar.netlify.app/"
    availability = "Yes, I can confirm I am available to work full time (10 am to 7 pm) for the next 3-6 months."

    html_body = f"""
    <html>
    <body>
        <p>Dear Hiring Team,</p>
        <p>Please find my submission for the Python (Selenium) Assignment.</p>
        <p>As requested, here are the 6 items:</p>
        <ol>
            <li><b>Screenshot:</b> Attached to this email ({SCREENSHOT_FILE}).</li>
            <li><b>Source Code (GitHub):</b> <a href="{github_link}">{github_link}</a></li>
            <li><b>Brief Documentation:</b> Included in the README.md in the GitHub repository.</li>
            <li><b>My Resume:</b> <a href="{resume_link}">Click to view my resume</a>.</li>
            <li><b>Past Projects/Work Samples:</b> <a href="{projects_link}">Click to view my portfolio</a>.</li>
            <li><b>Availability Confirmation:</b> {availability}</li>
        </ol>
        <p>The Google Form was filled automatically using Selenium, including handling the dynamic CAPTCHA. This email was sent via a Flask script as required.</p>
        <p>Thank you for the opportunity.</p>
        <p>Best regards,<br>{YOUR_NAME}</p>
    </body>
    </html>
    """
    return html_body

@app.route("/send-email")
def send_assignment_email():
    try:
        msg = MIMEMultipart()
        msg['From'] = YOUR_EMAIL
        msg['To'] = TO_EMAIL
        msg['Cc'] = CC_EMAIL
        msg['Subject'] = SUBJECT

        msg.attach(MIMEText(create_email_body(), 'html'))

        # Attach the screenshot
        with open(SCREENSHOT_FILE, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= {SCREENSHOT_FILE}")
        msg.attach(part)
        print("Email message created and attachment added.")

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(YOUR_EMAIL, YOUR_APP_PASSWORD)
        
        recipients = [TO_EMAIL] + [CC_EMAIL]
        server.sendmail(YOUR_EMAIL, recipients, msg.as_string())
        server.quit()
        
        print("Email sent successfully!")
        return "<h1>Email sent successfully!</h1>"

    except FileNotFoundError:
        print(f"Error: Could not find {SCREENSHOT_FILE}. Run fill_form.py first.")
        return f"<h1>Error: Could not find {SCREENSHOT_FILE}. Run fill_form.py first.</h1>"
    except Exception as e:
        print(f"Error: {e}")
        return f"<h1>Failed to send email: {e}</h1>"

if __name__ == "__main__":
    print("Flask server running. To send your email, open this URL in your browser:")
    print("http://127.0.0.1:5000/send-email")
    app.run(debug=True, port=5000, use_reloader=False) # use_reloader=False prevents it from running twice
