import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Custom Wait Condition ---
class wait_for_text_to_be_present(object):
    """
    An expectation for checking that an element has non-empty text.
    """
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element_text = driver.find_element(*self.locator).text.strip()
            return element_text != ""
        except:
            return False

# --- CONFIGURATION ---
FORM_URL = "https://forms.gle/WT68aV5UnPajeoSc8"
SCREENSHOT_PATH = "confirmation.png"

# --- YOUR DETAILS ---
TEXT_FIELDS = {
    "full_name": "Sulogno Sarkar",
    "contact": "8016980957",
    "email": "rhitsarkar2003@gmail.com",
    "address": "1 no, Mankumari road sutirmath Berhampore, Murshidabad, Westbengal",
    "pincode": "742101",
    "gender": "Male"
}

DOB_FULL = "08-11-2004" 

# --- ROBUST XPATH SELECTORS ---
XPATHS = {
    "full_name": "//div[@role='listitem' and .//span[contains(text(), 'Full Name')]]//input[@type='text']",
    "contact": "//div[@role='listitem' and .//span[contains(text(), 'Contact Number')]]//input[@type='text']",
    "email": "//div[@role='listitem' and .//span[contains(text(), 'Email ID')]]//input[@type='text']",
    "address": "//div[@role='listitem' and .//span[contains(text(), 'Full Address')]]//textarea",
    "pincode": "//div[@role='listitem' and .//span[contains(text(), 'Pin Code')]]//input[@type='text']",
    "gender": "//div[@role='listitem' and .//span[contains(text(), 'Gender')]]//input[@type='text']",
    "dob": "//input[@type='date']",
    
    # Using a more specific XPath for the CAPTCHA text
    "captcha_text": "//span[contains(text(), 'Type this code:')]//b", 
    "captcha_input": "//div[@role='listitem' and .//div[contains(., 'Type this code:')]]//input[@type='text']",
    
    "submit_button": "//span[text()='Submit']"
}

def fill_google_form():
    print("Starting browser...")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10) 

    try:
        driver.get(FORM_URL)
        print("Form loaded. Filling fields...")

        # --- 1. FILL ALL TEXT FIELDS ---
        for key, value in TEXT_FIELDS.items():
            try:
                field = wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS[key])))
                field.send_keys(value)
                print(f"Filled '{key}'")
            except Exception as e:
                print(f"Could not fill '{key}': {e}")
        
        # --- 2. FILL DATE OF BIRTH ---
        print("Filling Date of Birth...")
        try:
            date_field = wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS["dob"])))
            date_field.send_keys(DOB_FULL)
            print("Filled Date of Birth.")
        except Exception as e:
             print(f"Could not fill Date of Birth: {e}")

        # --- 3. HANDLE CAPTCHA (*** THIS IS THE FIX ***) ---
        try:
            print("Waiting for CAPTCHA code to appear...")
            # Use our custom wait condition
            wait.until(wait_for_text_to_be_present((By.XPATH, XPATHS["captcha_text"])))
            
            # Now that we know text exists, we can read it
            captcha_code = driver.find_element(By.XPATH, XPATHS["captcha_text"]).text.strip()
            
            if not captcha_code:
                raise Exception("CAPTCHA text was found but is empty!")
                
            print(f"Found CAPTCHA code: {captcha_code}")

            captcha_input = driver.find_element(By.XPATH, XPATHS["captcha_input"])
            captcha_input.send_keys(captcha_code)
            print("Filled CAPTCHA.")
        except Exception as e:
            print(f"Could not solve CAPTCHA: {e}")
            raise # Stop if CAPTCHA fails

        # --- 4. SUBMIT ---
        print("Submitting form...")
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, XPATHS["submit_button"])))
        submit_button.click()
        
        print("Form submitted. Waiting for confirmation...")
        time.sleep(3) 
        driver.save_screenshot(SCREENSHOT_PATH)
        print(f"Screenshot saved to {SCREENSHOT_PATH}")

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.save_screenshot("error_screenshot.png") 
        print("Saved error_screenshot.png for debugging.")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    fill_google_form()
