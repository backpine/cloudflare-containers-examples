import logging
import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import subprocess
import tempfile
import uuid

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def handleLogic():
    return

MESSAGE = os.environ.get("MESSAGE", "Hello, World!")
CLOUDFLARE_LOCATION = os.environ.get("CLOUDFLARE_LOCATION", "Unknown")
CLOUDFLARE_COUNTRY_A2 = os.environ.get("CLOUDFLARE_COUNTRY_A2", "Unknown")
CLOUDFLARE_DEPLOYMENT_ID = os.environ.get("CLOUDFLARE_DEPLOYMENT_ID", "Unknown")
CLOUDFLARE_NODE_ID = os.environ.get("CLOUDFLARE_NODE_ID", "Unknown")
CLOUDFLARE_PLACEMENT_ID = os.environ.get("CLOUDFLARE_PLACEMENT_ID", "Unknown")
CLOUDFLARE_REGION = os.environ.get("CLOUDFLARE_REGION", "Unknown")

@app.get("/")
def hello_world():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}

@app.get("/python-container")
def python_container():
    logger.info("Python container direct request")
    os.environ.get("PYTHONPATH")
    handleLogic()
    return {"Message": MESSAGE, "Cloudflare Location": CLOUDFLARE_LOCATION}

@app.get("/load-balance")
def load_balance():
    logger.info("Load balance endpoint accessed")
    return {
        "Message": MESSAGE,
        "Cloudflare Location": CLOUDFLARE_LOCATION,
        "Cloudflare Country": CLOUDFLARE_COUNTRY_A2,
        "Cloudflare Deployment ID": CLOUDFLARE_DEPLOYMENT_ID,
        "Cloudflare Region": CLOUDFLARE_REGION
    }


@app.get("/video-upload", response_class=HTMLResponse)
def video_upload_form():
    logger.info("Video upload form accessed")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Video Upload</title>
    </head>
    <body>
        <h1>Upload Video for 2x Speed Processing</h1>
        <form action="/process-video" method="post" enctype="multipart/form-data">
            <input type="file" name="video" accept="video/*" required>
            <button type="submit">Upload and Process</button>
        </form>
    </body>
    </html>
    """

@app.post("/process-video")
async def process_video(video: UploadFile = File(...)):
    logger.info(f"Video processing started for file: {video.filename}")

    if not video.content_type or not video.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")

    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as input_file:
        input_path = input_file.name
        content = await video.read()
        input_file.write(content)

    output_path = f"/tmp/{uuid.uuid4()}_2x_speed.mp4"

    try:
        # Use ffmpeg to speed up video by 2x
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-filter:v', 'setpts=0.5*PTS',
            '-filter:a', 'atempo=2.0',
            '-y',  # overwrite output file
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr}")
            raise HTTPException(status_code=500, detail="Video processing failed")

        logger.info("Video processing completed successfully")

        # Return the processed video
        return FileResponse(
            output_path,
            media_type='video/mp4',
            filename=f"2x_speed_{video.filename}"
        )

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail="Video processing failed")

    finally:
        # Clean up input file
        if os.path.exists(input_path):
            os.unlink(input_path)


@app.exception_handler(404)
def custom_not_found_handler(request, exc):
    logger.info(f"404 Not Found: {request.url}")
    return {"error": "Not Found", "message": "The requested resource was not found"}
