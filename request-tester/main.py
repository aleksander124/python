import requests
import time
import urllib3

# Suppress only the InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def open_site(url, times, interval):
    for i in range(times):
        try:
            # Set verify to False to ignore SSL certificate validation
            response = requests.get(url, verify=False)
            print(f"Request {i+1}: Status Code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request {i+1}: Failed with exception {e}")
        time.sleep(interval)

if __name__ == "__main__":
    url = "https://helloworld.apps.openshift-dev.mednet.world/hello"  # Replace with your target URL
    times = 1000
    interval = 0.01  # in seconds

    open_site(url, times, interval)
