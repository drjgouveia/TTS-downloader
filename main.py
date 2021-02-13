import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import pathlib
from selenium.webdriver.chrome.options import Options

filePath = str(pathlib.Path(__file__).parent.absolute()) + "\\"
i = 1

chrome_options = Options()
prefs = {'profile.default_content_setting_values.automatic_downloads': 1, "download.default_directory": filePath}
chrome_options.add_experimental_option("prefs", prefs)
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps, options=chrome_options)
driver.get('https://www.naturalreaders.com/online/')


def save_audio_file(url):
    global i, filePath
    try:
        javascript = f'a = document.createElement("a"); a.href = "{url}"; a.download = "{i}"; a.click();'
        driver.execute_script(javascript)
        i += 1
    except Exception as e:
        print(str(e))


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response


def process_requests(url):
    try:
        if "blob" in url["params"]["response"]["url"]:
            print(url["params"]["response"]["url"])
            save_audio_file(url["params"]["response"]["url"])
            return url["params"]["response"]["url"]

    except Exception as e:
        pass


while True:
    try:
        browser_log = driver.get_log('performance')
        events = [process_browser_log_entry(entry) for entry in browser_log]
        events = [event for event in events if 'Network.responseReceived' in event['method']]
        events = [process_requests(event) for event in events]

        x = driver.current_url
    except Exception as e:
        print(str(e))
        driver.quit()
        break
