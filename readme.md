# Coursera Quiz Solver Automation using Gemini

This project allows you to automate the process of answering Coursera quizzes using the Gemini model. It extracts multiple-choice questions (MCQs) from the quiz, sends them to the Gemini API for answers, selects the correct options on the page, and submits the quiz.

---

### Video Demo:

Here's a quick demonstration of how the Coursera Quiz Solver works:

https://github.com/AnishaShende/Unethical/blob/578c464a4d2d721ba58215c1abaa2f1cb9ab7bcd/assets/Screen%20Recording%202025-04-16%20014258%20(1).mp4

---

### Prerequisites:

- **Python 3.x**
- **Selenium**: To control the Chrome browser programmatically.
- **Gemini API Key**: For sending quiz questions to Gemini and receiving answers.
- **ChromeDriver**: Required to interface with Chrome through Selenium.

---

## Setup Instructions:

### 1. **Install Python & Required Libraries**

Make sure you have Python 3.x installed. You can download it from [here](https://www.python.org/downloads/).

Once you have Python installed, create a virtual environment for your project:

```bash
python -m venv .venv
```

Activate the virtual environment:

- On Windows:
  ```bash
  .venv\Scripts\activate
  ```
- On Mac/Linux:
  ```bash
  source .venv/bin/activate
  ```

Install the necessary libraries:

```bash
pip install selenium requests undetected-chromedriver
```

### 2. **Download ChromeDriver**

To use Selenium with Chrome, you'll need **ChromeDriver** which is a separate executable that Selenium uses to control Chrome. You can download it from [here](https://sites.google.com/a/chromium.org/chromedriver/).

Make sure you download the version that matches your Chrome browser version.

### 3. **Configure Chrome to Allow Debugging**

You need to allow Selenium to interact with your existing Chrome profile. Here’s how:

#### Step 1: Start Chrome with Remote Debugging

1. Close all instances of Chrome.
2. Open a command prompt or terminal and run the following command:

   On Windows:

  (General)
   ```bash
   chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-temp"
   ```
  (Use below command [replace your username] also check your profile name in case of multiple profiles on chrome)
  ```bash
  "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\[Anisha]\AppData\Local\Google\Chrome\User Data" --profile-directory="Profile 2"
  ```
   On Mac/Linux:

   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-temp"
   ```

   This opens Chrome with remote debugging enabled. Chrome will use the `chrome-temp` directory for your profile data. If you want to use a specific profile, modify the `--user-data-dir` argument to point to that profile directory (e.g., `"C:\Users\<User>\AppData\Local\Google\Chrome\User Data"`).

#### Step 2: Start Selenium with the Debugger

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument(f"--user-data-dir=path_to_your_chrome_user_data")

# Launch the browser in headless mode
driver = uc.Chrome(options=chrome_options)
```

---

### 4. **Obtain a Gemini API Key**

To interact with the Gemini model, you’ll need an API key. If you don't have it already, you need to get access to Gemini or use an available key if provided by someone else. Refer to the official documentation for more details on getting the API key.

---

## Script Setup and Usage:

### 1. **Set Up the Script**

After cloning or downloading the repository, update the following in the script:

- Replace `"your_gemini_api_key"` with your actual Gemini API key in the script.
- Adjust the `driver_path` in the code to where you have stored `chromedriver`.

### 2. **Running the Script**

Run the script using the command below:

```bash
python script.py
```
(script2.py for quiz and script3.py for video automation)

After executing, when prompted enter the url of the quiz webpage after clicking on start quiz button.
Example link: https://www.coursera.org/learn/application-security-for-developers-devops/assignment-submission/SBoXR/graded-quiz-final-project/attempt

This will:

- Open Chrome with your profile using the remote debugging port.
- Navigate to the quiz page.
- Extract the MCQs.
- Send the questions to Gemini.
- Receive the answers.
- Select the correct options on the page.
- Submit the quiz.

### 3. **Ensure You Are Logged In**

Since the script uses your existing Chrome profile, make sure you are logged into Coursera before running the script. If you want to automate the login as well, you can modify the script to click on the "Continue with Google" button and log in using your Google credentials, as shown in the script.

---

## Troubleshooting:

### 1. **Remote Debugging Not Connecting**

If you’re seeing an error like `cannot connect to chrome at 127.0.0.1:9222`, ensure that:

- You have started Chrome with the correct debugging port.
- Chrome is running and listening on the specified port.
- The port is not blocked by a firewall.

### 2. **Page Elements Not Found**

If the script fails to locate questions or options on the page, inspect the page using Chrome DevTools (`Ctrl+Shift+I`) to ensure the correct selectors are being used in the script.

---

## License:

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Example Usage:

Once everything is set up and running, you'll be able to:

1. **Launch the script**: It will open Chrome, navigate to the quiz page, and extract questions.
2. **Get Gemini's Answer**: Gemini will provide the answers based on the questions.
3. **Select the answers**: The script will automatically select the answers in the quiz.
4. **Submit the quiz**: Once all answers are selected, the script will submit the quiz.

---

### Final Thoughts:

Disclaimer: This script is intended purely for fun and to assist with the learning process. Please use it responsibly. Always review the answers and make sure you understand the questions yourself. If you notice any errors or issues, feel free to reach out to me. 😊
