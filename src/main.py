import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from src.utilities import Utilities
from src.openai_client import OpenAIClient
import tempfile
import os
import traceback
import logging
from pydantic import BaseModel
from src.config import ALLOWED_FILE_EXTENSIONS, HOST, PORT

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
utilities = Utilities()
openai_client = OpenAIClient()


class CVAnalysisRequest(BaseModel):
    file_path: str


class AnalysisResponse(BaseModel):
    analysis: str


@app.post("/analyze-cv/", response_model=AnalysisResponse)
async def analyze_cv(request: CVAnalysisRequest, background_tasks: BackgroundTasks):
    file_path = request.file_path

    if not file_path.lower().endswith(ALLOWED_FILE_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please provide a path to a PDF or Word document.",
        )

    try:
        # Log file details
        logger.info(f"Attempting to read file: {file_path}")
        logger.info(f"File exists: {os.path.exists(file_path)}")
        logger.info(f"File size: {os.path.getsize(file_path)} bytes")

        # Process the CV
        cv_text = await asyncio.to_thread(utilities.read_cv, file_path)

        logger.info(f"File contents: {cv_text[:100]}")  # Print first 100 characters

        prompt = utilities.generate_prompt(cv_text)
        result = await openai_client.call_openai_api(prompt)

        if result is None:
            raise HTTPException(
                status_code=500, detail="Failed to get response from OpenAI API"
            )

        formatted_output = utilities.parse_and_format_output(result)

        return AnalysisResponse(analysis=formatted_output)

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An error occurred while processing the CV"
        )


async def cleanup_temp_file(file_path: str):
    try:
        os.unlink(file_path)
    except Exception as e:
        logger.error(f"Error deleting temporary file {file_path}: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
