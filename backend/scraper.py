from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_jobs(keyword):
    # Set up Selenium WebDriver with improved configuration
    options = Options()
    options.headless = True  # Run in headless mode (disable for debugging)
    options.add_argument("--disable-gpu")  # Disable GPU rendering
    options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
    options.add_argument("--use-gl=swiftshader")  # Force software WebGL for rendering

    # Replace with the actual path to your ChromeDriver
    service = Service(r"C:\Users\hp\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Target URL for scraping
        url = f"https://wellfound.com/jobs?keywords={keyword}"
        driver.get(url)  # Load the webpage
        driver.implicitly_wait(10)  # Wait for the page to load

        # Parse the rendered HTML with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        jobs = []

        # Extract job information
        for job_card in soup.find_all("div", class_="styles_component__7_YVb"):
            company_name = job_card.find("h2", class_="inline text-md font-semibold")
            job_description = job_card.find("span", class_="text-md text-neutral-1000")
            company_size = job_card.find("span", class_="text-xs italic text-neutral-500")

            if company_name and job_description and company_size:
                jobs.append({
                    "company": company_name.text.strip(),
                    "description": job_description.text.strip(),
                    "size": company_size.text.strip()
                })

        return jobs

    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return []

    finally:
        driver.quit()  # Ensure the browser is closed