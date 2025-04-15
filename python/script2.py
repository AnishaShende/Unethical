import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

from dotenv import load_dotenv

load_dotenv()

# def human_typing(element, text):
#     for char in text:
#         element.send_keys(char)
#         time.sleep(random.uniform(0.1, 0.2)) 

# options = uc.ChromeOptions()
# options.add_argument("--disable-blink-features=AutomationControlled")
# driver = uc.Chrome(options=options)


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=chrome_options)


# Step 1: Open the window/browser
# driver = webdriver.Chrome()  # or use Edge/Firefox depending on your setup
driver.get("https://www.coursera.org/learn/agile-development-and-scrum/assignment-submission/FJ6oK/practice-quiz/attempt")
time.sleep(10)

# # Scroll randomly
# driver.execute_script("window.scrollBy(0, 300)")

# # Move mouse
# actions = ActionChains(driver)
# actions.move_by_offset(100, 100).perform()

# # Step 2: Enter login credentials
# # Select email input using data-e2e attribute
# email_input = driver.find_element(By.CSS_SELECTOR, '[data-e2e="login-email-input"]')
# # email_input.send_keys("xxxxxx")
# human_typing(email_input, "xxxxxx")

# time.sleep(2)
# # Similarly find the password field (share HTML if you need help with that too)
# password_input = driver.find_element(By.CSS_SELECTOR, '[data-e2e="login-password-input"]')
# # password_input.send_keys("xxxxxx")
# human_typing(password_input, "xxxxxx")
# time.sleep(3)
# password_input.send_keys(Keys.RETURN)



# Click the "Log in" or "Sign in" button if needed
# try:
#     login_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Log In')]")
#     login_btn.click()
#     time.sleep(3)
# except:
#     pass

# # Click "Continue with Google"
# google_btn = driver.find_element(By.XPATH, "//button[contains(.,'Continue with Google')]")
# google_btn.click()

# input("Solve the CAPTCHA manually and press Enter to continue...")

# Step 3: Wait for page to load (simple wait or better with WebDriverWait)
# time.sleep(15)  # You can use WebDriverWait for a more dynamic wait

# Step 4: Now you are on the Test Page - Start extracting
# test_data = driver.find_element(By.ID, "test-content").text
# element = driver.find_element(By.CSS_SELECTOR, '[data-testid="part-Submission_MultipleChoiceQuestion"]')
# print(element.text)


# # === 3. Extract MCQs ===
# question_blocks = driver.find_elements(By.CSS_SELECTOR, "[data-testid='part-Submission_MultipleChoiceQuestion']")
# questions = []

# for block in question_blocks:
#     try:
#         question_text = block.find_element(By.CSS_SELECTOR, "[data-testid='cml-viewer']").text.strip()
#     except:
#         question_text = "N/A"

#     options = []
#     labels = block.find_elements(By.CSS_SELECTOR, "label.cui-Checkbox")
#     for label in labels:
#         try:
#             option = label.find_element(By.CSS_SELECTOR, "[data-testid='cml-viewer']").text.strip()
#         except:
#             option = "N/A"
#         is_checked = "cui-isChecked" in label.get_attribute("class")
#         options.append({"text": option, "selected": is_checked})

#     questions.append({"question": question_text, "options": options})

# Extract questions and options
questions_data = []

question_blocks = driver.find_elements(By.CSS_SELECTOR, '[data-testid="part-Submission_MultipleChoiceQuestion"]')
for block in question_blocks:
    try:
        question_text = block.find_element(By.CSS_SELECTOR, '[data-testid="cml-viewer"]').text.strip()
        options = []
        labels = block.find_elements(By.CSS_SELECTOR, "label.cui-Checkbox")
        for label in labels:
            try:
                option_text = label.find_element(By.CSS_SELECTOR, '[data-testid="cml-viewer"]').text.strip()
                is_selected = "cui-isChecked" in label.get_attribute("class")
                options.append({"text": option_text, "selected": is_selected})
            except:
                continue
        questions_data.append({"question": question_text, "options": options})
    except:
        continue

# Display the extracted data
print("\nExtracted Questions:")
print(json.dumps(questions_data, indent=2, ensure_ascii=False))

# Step 5: Send to LLM (example using requests)
import requests
# response = requests.post("http://localhost:8000/query", json={"text": test_data})
# === 4. Send to Gemini API ===
api_key = os.getenv("GEMINI_API_KEY")  # Replace with your actual key
# gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

def ask_gemini(question_text, options_list, api_key):
    prompt = f"""You are a helpful assistant. Choose the most appropriate answer.
Question: {question_text}
Options:"""
    for idx, opt in enumerate(options_list):
        prompt += f"{idx + 1}. {opt}\n"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
        headers={"Content-Type": "application/json"},
        json=payload
    )

    try:
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()
    except Exception as e:
        print(f"Error from Gemini: {e}")
        return ""

time.sleep(1)

for i, block in enumerate(question_blocks):
    try:
        question_text = questions_data[i]["question"]
        option_texts = [opt["text"] for opt in questions_data[i]["options"]]

        print(f"\nSending Q{i+1} to Gemini...")
        answer = ask_gemini(question_text, option_texts, api_key)
        print("Gemini answered:", answer)

        time.sleep(1)

        # Match the Gemini answer to an option
        selected_index = -1
        for idx, option in enumerate(option_texts):
            if option.lower() in answer.lower() or answer.lower() in option.lower():
                selected_index = idx
                break

        if selected_index == -1:
            print("❌ Could not match Gemini's response to any option")
            continue

        # Select the matched checkbox
        labels = block.find_elements(By.CSS_SELECTOR, "label.cui-Checkbox")
        if selected_index < len(labels):
            driver.execute_script("arguments[0].click();", labels[selected_index])
            print(f"✅ Selected option {selected_index + 1}: {option_texts[selected_index]}")
        else:
            print("❌ Matched index out of range")

    except Exception as e:
        print(f"Error on Q{i+1}: {e}")

# Step 4: Submit the quiz
def submit_quiz(driver):
    submit_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="submit-button"]')
    submit_button.click()
    print("🚀 Quiz Submitted!")


# Step 6: Close the browser when done
# driver.quit()
