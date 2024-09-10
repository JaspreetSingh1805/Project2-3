from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import time

# Set up the Selenium WebDriver (assuming you're using Chrome, update if using another browser)
driver = webdriver.Chrome()

# Open the website
url = "http://books.toscrape.com/catalogue/page-1.html"
driver.get(url)

# Create or open a CSV file to store the data
with open('books.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Title', 'Price', 'Availability'])  # Header row

    # Iterate over multiple pages
    while True:
        # Wait for a few seconds to ensure the page is fully loaded
        time.sleep(2)
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find all book listings
        books = soup.find_all('article', class_='product_pod')
        
        # Loop through all books on the page
        for book in books:
            # Get the book title
            title = book.h3.a['title']
            
            # Get the book price
            price = book.find('p', class_='price_color').text
            
            # Get the availability
            availability = book.find('p', class_='instock availability').text.strip()
            
            # Write the book data to the CSV file
            csv_writer.writerow([title, price, availability])
        
        # Find the 'next' button on the page
        next_button = soup.find('li', class_='next')
        
        # If there is a next button, navigate to the next page
        if next_button:
            next_page_url = next_button.a['href']
            next_page_url = url.rsplit('/', 1)[0] + '/' + next_page_url
            driver.get(next_page_url)
        else:
            # If there are no more pages, exit the loop
            break

# Close the browser after scraping
driver.quit()