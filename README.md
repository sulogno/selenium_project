Python (Selenium) Assignment - The Medius

This project is a complete solution for the hiring assignment, which involves:

Automatically filling a specific Google Form using Selenium.

Handling all fields, including text, date, and a dynamic CAPTCHA.

Sending a confirmation email with all required items (screenshot, links, resume) using Flask and smtplib.

1. Form Automation (fill_form.py)

This script launches a Chrome browser, navigates to the Google Form, and intelligently fills all fields.

Key Features:

Robust Selectors: Uses stable, relative XPaths (e.g., //div[contains(., 'Full Name')]...) to find form elements. This method is resistant to minor HTML changes, unlike fragile absolute XPaths.

Handles All Field Types:

Text/Textarea: Fills standard text inputs and text areas.

Date Field: Correctly identifies the <input type="date"> element and sends a YYYY-MM-DD formatted string.

Advanced CAPTCHA Handling: The script successfully bypasses the "xfanatical" CAPTCHA using a multi-step process:

Custom Wait Condition: It uses a custom Python class wait_for_text_to_be_present to pause the script until the dynamic CAPTCHA text (e.g., GNFPYC) has fully loaded on the page.

Scraping: It then reads the .text from the <b> tag containing the code.

Input: Finally, it types the scraped code into the CAPTCHA's input box.

Confirmation: Upon successful submission, it waits for the confirmation page and saves a screenshot named confirmation.png.

2. Email Submission (send_email.py)

This script fulfills the requirement to send the submission email via code.

Key Features:

Flask Web Server: Creates a simple Flask server with a single endpoint (/send-email). This allows the email-sending logic to be triggered by visiting a URL.

SMTP Integration: Uses Python's built-in smtplib to connect to Gmail's SMTP server (smtp.gmail.com) over a secure TLS connection.

Secure Authentication: Uses a Google App Password for login, which is the modern, secure standard for programmatic email sending (as regular passwords are no longer supported by Google for this).

MIME Email Construction: Builds a MIMEMultipart email, allowing for both a rich HTML body and file attachments.

Full Submission: The HTML body is formatted to include all 6 required items:

The attached screenshot.

A link to the GitHub repository.

This README.md as documentation.

A link to the candidate's resume.

A link to a portfolio/projects.

Confirmation of availability.

Attachment: The confirmation.png file is read from the disk and attached to the email.

How to Run This Project

Follow these steps to run the automation and send the submission email.

Prerequisites

Python 3

Google Chrome browser

ChromeDriver (must match your Chrome version)

A Google Account with 2-Step Verification and an App Password.

Step 1: Clone the Repository

git clone [https://github.com/sulogno/selenium_project.git](https://github.com/sulogno/selenium_project.git)
cd selenium_project


Step 2: Install Dependencies

pip install selenium flask


Step 3: Run the Form Filler

This script will run the browser automation and generate the confirmation.png screenshot.

python fill_form.py


(Wait for it to complete. You will see "Screenshot saved to confirmation.png" in your terminal.)

Step 4: Configure and Run the Email Sender

Edit the file send_email.py:

Update YOUR_EMAIL with your Gmail address.

Update YOUR_APP_PASSWORD with your 16-digit Google App Password.

Run the Flask server:

python send_email.py


Trigger the Email:

Your terminal will show: * Running on http://127.0.0.1:5000

Open your web browser and go to this exact URL:
http://127.0.0.1:5000/send-email

This will trigger the script, send the email, and display "Email sent successfully!" in your browser.
