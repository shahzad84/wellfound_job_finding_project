from fastapi import FastAPI, HTTPException
from scraper import scrape_jobs
from threading import Thread, Lock

app = FastAPI()

job_data = []  # Global variable to store job data
scraping_in_progress = False  # Flag to indicate if scraping is ongoing
lock = Lock()  # Lock to ensure thread safety for shared resources

def update_jobs(keyword):
    global job_data, scraping_in_progress
    try:
        with lock:
            scraping_in_progress = True  # Set flag to indicate scraping is in progress
        result = scrape_jobs(keyword)  # Perform the actual scraping
        with lock:
            job_data.clear()  # Clear previous data
            job_data.extend(result)  # Update job data with new data
    finally:
        with lock:
            scraping_in_progress = False  # Reset flag once scraping is complete

@app.get("/scrape")
def scrape(keyword: str):
    global scraping_in_progress
    with lock:
        if scraping_in_progress:
            raise HTTPException(status_code=400, detail="Scraping is already in progress. Please wait.")

    try:
        # Start the scraping process in a separate thread
        thread = Thread(target=update_jobs, args=(keyword,))
        thread.daemon = True  # Make the thread a daemon so it exits when the main program exits
        thread.start()
        return {"message": "Scraping initiated. Please fetch results in a few seconds."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/jobs")
def get_jobs():
    with lock:
        if not job_data:
            raise HTTPException(status_code=404, detail="No data available. Please initiate scraping.")
    
    return {"jobs": job_data}



# uvicorn app:app --reload