import logging
import os

from fastapi import FastAPI

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

MESSAGE = os.environ.get("MESSAGE", "Hello, World!")
CLOUDFLARE_LOCATION = os.environ.get("CLOUDFLARE_LOCATION", "Unknown")
CLOUDFLARE_COUNTRY_A2 = os.environ.get("CLOUDFLARE_COUNTRY_A2", "Unknown")
CLOUDFLARE_DEPLOYMENT_ID = os.environ.get("CLOUDFLARE_DEPLOYMENT_ID", "Unknown")
CLOUDFLARE_NODE_ID = os.environ.get("CLOUDFLARE_NODE_ID", "Unknown")
CLOUDFLARE_PLACEMENT_ID = os.environ.get("CLOUDFLARE_PLACEMENT_ID", "Unknown")
CLOUDFLARE_REGION = os.environ.get("CLOUDFLARE_REGION", "Unknown")

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}

@app.get("/python-container")
def read_health():
    logger.info("Python container direct request")
    os.environ.get("PYTHONPATH")
    return {"Message": MESSAGE, "Cloudflare Location": CLOUDFLARE_LOCATION}

@app.get("/load-balance")
def load_balance():
    logger.info("Load balance endpoint accessed")
    return {
        "Message": MESSAGE,
        "Cloudflare Location": CLOUDFLARE_LOCATION,
        "Cloudflare Country": CLOUDFLARE_COUNTRY_A2,
        "Cloudflare Deployment ID": CLOUDFLARE_DEPLOYMENT_ID,
        "Cloudflare Node ID": CLOUDFLARE_NODE_ID,
        "Cloudflare Placement ID": CLOUDFLARE_PLACEMENT_ID,
        "Cloudflare Region": CLOUDFLARE_REGION
    }

@app.exception_handler(404)
def custom_not_found_handler(request, exc):
    logger.info(f"404 Not Found: {request.url}")
    return {"error": "Not Found", "message": "The requested resource was not found"}
