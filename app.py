from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None, "error": None})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, url: str = Form(...)):
    result = None
    error = None

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(5)

    try:
        result = {
            'reg_year': driver.find_element(By.XPATH, "//p[text()='Reg. year']/following-sibling::p").text,
            'fuel_type': driver.find_element(By.XPATH, "//p[text()='Fuel']/following-sibling::p").text,
            'km_driven': driver.find_element(By.XPATH, "//p[text()='KM driven']/following-sibling::p").text,
            'transmission': driver.find_element(By.XPATH, "//p[text()='Transmission']/following-sibling::p").text,
            'ownership': driver.find_element(By.XPATH, "//p[text()='Ownership']/following-sibling::p").text,
            'make_year': driver.find_element(By.XPATH, "//p[text()='Make year']/following-sibling::p").text,
            'spare_key': driver.find_element(By.XPATH, "//p[text()='Spare key']/following-sibling::p").text,
            'reg_number': driver.find_element(By.XPATH, "//p[text()='Reg number']/following-sibling::p").text,
            'car_price': driver.find_element(By.XPATH, "//div[contains(@class, 'styles_price__')]/p").text
        }
    except Exception as e:
        error = f"Error while scraping: {e}"
    finally:
        driver.quit()

    return templates.TemplateResponse("index.html", {"request": request, "result": result, "error": error})