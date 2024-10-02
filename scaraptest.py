import os
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Install ChromeDriver automatically
chromedriver_autoinstaller.install()

def get_video_recommendations(search_term):
    if not search_term:
        raise ValueError("No search term provided")

    search_query = f"{search_term} site:youtube.com"
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

        return results
    
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching video recommendations: {str(e)}")
    
    finally:
        driver.quit()  # Ensure driver is closed properly

# Example of how to use the function
if __name__ == '__main__':
    try:
        search_input = input("Enter a search term for YouTube: ")
        recommendations = get_video_recommendations(search_input)
        for video in recommendations:
            print(f"Title: {video['title']}\nLink: {video['link']}\n")
    except Exception as e:
        print(f"Error: {e}")
