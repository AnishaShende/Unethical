from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

# --- Your links go here ---
links = [
    "https://www.coursera.org/learn/test-and-behavior-driven-development-tdd-bdd/lecture/QKSUR/the-importance-of-testing",
    "https://www.coursera.org/learn/test-and-behavior-driven-development-tdd-bdd/lecture/91maE/running-tests-with-nose"
]

# Setup Chrome to connect with debugging instance
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

# --- Loop through all links ---
for link in links:
    print(f"\n📂 Starting module: {link}")
    driver.get(link)
    time.sleep(5)  # Allow time for page to load

    visited_indexes = set()

    while True:
        # Get all video list items
        video_items = driver.find_elements(By.XPATH, "//span[contains(text(),'Video')]/ancestor::li")
        found_next = False

        for idx, item in enumerate(video_items):
            if idx in visited_indexes:
                continue

            html = item.get_attribute("innerHTML").lower()
            if "check" in html or "cds-checkmark" in html:
                visited_indexes.add(idx)
                continue

            visited_indexes.add(idx)
            found_next = True

            print(f"🎯 Clicking video #{idx + 1}")
            driver.execute_script("arguments[0].scrollIntoView();", item)
            item.click()

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                time.sleep(2)
                video_tag = driver.find_element(By.TAG_NAME, "video")
                duration = driver.execute_script("return arguments[0].duration;", video_tag)
                if duration and duration > 5:
                    seek_time = duration * 0.98
                    driver.execute_script("arguments[0].currentTime = arguments[1];", video_tag, seek_time)
                    print(f"⏩ Seeking to {int(seek_time)}s of {int(duration)}s")
                    wait_time = max(duration - seek_time + 2, 8)
                    time.sleep(wait_time)
                else:
                    print("⚠️ Video too short or duration unavailable.")
            except Exception as e:
                print(f"❌ Error playing video: {e}")

            break  # Go back to while loop and refresh the list

        if not found_next:
            print("✅ All videos in this module completed.")
            break

print("\n🎉 All modules completed!")