import os
import re
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

# Initialize Flask app
app = Flask(__name__)

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Install ChromeDriver automatically
chromedriver_autoinstaller.install()

# Define Flask routes
@app.route('/')
def index():
    return "<h1>YouTube Search API</h1>"

@app.route('/api', methods=['GET'])
def api():
    message = request.args.get('msg')
    if not message:
        return jsonify({"error": "No message provided"}), 400

    search_query = f"{message} site:youtube.com"
    url = "https://www.youtube.com/results"

    # Set up the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(search_query)
        search_box.submit()

        driver.implicitly_wait(10)  # Wait for the page to load

        # Parse the page with BeautifulSoup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Extract search results
        results = []
        title_elements = soup.find_all('h3', class_='title-and-badge')  # Adjust class based on YouTube's structure
        for title_element in title_elements:
            title = title_element.get_text()
            link = title_element.find('a')['href'] if title_element.find('a') else "N/A"
            results.append({
                'title': title,
                'link': f"https://www.youtube.com{link}" if link else "N/A",
            })
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        driver.quit()  # Ensure driver is closed properly

# Run the Flask app
if __name__ == '__main__':
    app.run(port=7488)
