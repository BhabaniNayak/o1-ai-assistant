# O-1A Visa Eligibility Analyzer

This project is an AI-powered tool that analyzes a candidate's CV to assess their eligibility for an O-1A visa. It uses OpenAI's GPT model to evaluate the CV against the O-1A visa criteria and provide a detailed analysis.

## Project Structure

The project consists of the following key files in src directory:

1. `main.py`: The main FastAPI application file.
2. `utilities.py`: Contains utility functions for CV processing and output formatting.
3. `openai_client.py`: Handles communication with the OpenAI API.
4. `config.py`: Stores configuration variables and constants.
5. `Dockerfile`: Defines the Docker container for the application.
6. `pyproject.toml`: Specifies project dependencies using Poetry.
7. `test.ipynb`: A Jupyter notebook for testing the application components.

## Architecture

The application follows a modular architecture:

1. **FastAPI Application** (`main.py`):
   - Defines the API endpoint for CV analysis.
   - Handles file uploads and coordinates the analysis process.

2. **Utilities** (`utilities.py`):
   - Provides functions for reading CV files (PDF and DOCX).
   - Generates prompts for the OpenAI API.
   - Parses and formats the API response.

3. **OpenAI Client** (`openai_client.py`):
   - Manages communication with the OpenAI API.
   - Implements retry logic for API calls.

4. **Configuration** (`config.py`):
   - Centralizes configuration variables and constants.
   - Uses environment variables for sensitive information.

5. **Docker Container** (`Dockerfile`):
   - Defines a containerized environment for the application.

## Setup and Running Locally

To run the application locally, follow these steps:

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd o1a-visa-analyzer
   ```

2. **Install Poetry:**
   ```
   pip install poetry
   ```

3. **Install dependencies:**
   ```
   poetry install
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

5. **Run the application:**
   ```
   poetry run uvicorn src.main:app --reload
   ```

   The application will be available at `http://localhost:8000`.

6. **Test the API:**
   Use a tool like cURL or Postman to send a POST request to `http://localhost:8000/analyze-cv/` with a CV file attached.
   
   Example Request:
   curl -v -X POST http://localhost:8001/analyze-cv/ \
   -H "Content-Type: application/json" \
   -d '{"file_path": "provide_the_path"}'

   Sample Response:
   {"analysis":"Raw content:\n{\n  \"title\": \"OutputSchema\",\n  \"type\": \"object\",\n  \"properties\": {\n    \"criteria_analysis\": {\n      \"title\": \"Criteria Analysis\",\n      \"type\": \"array\",\n      \"items\": {\n        \"$ref\": \"#/definitions/CriterionAnalysis\"\n      }\n    },\n    \"overall_summary\": {\n      \"title\": \"Overall Summary\",\n      \"type\": \"string\"\n    },\n    \"rating\": {\n      \"title\": \"Rating\",\n      \"type\": \"string\"\n    }\n  },\n  \"required\": [\n    \"criteria_analysis\",\n    \"overall_summary\",\n    \"rating\"\n  ],\n  \"definitions\": {\n    \"CriterionAnalysis\": {\n      \"title\": \"CriterionAnalysis\",\n      \"type\": \"object\",\n      \"properties\": {\n        \"criterion\": {\n          \"title\": \"Criterion\",\n          \"type\": \"string\"\n        },\n        \"achievements\": {\n          \"title\": \"Achievements\",\n          \"type\": \"array\",\n          \"items\": {\n            \"type\": \"string\"\n          }\n        },\n        \"explanation\": {\n          \"title\": \"Explanation\",\n          \"type\": \"string\"\n        }\n      },\n      \"required\": [\n        \"criterion\",\n        \"achievements\",\n        \"explanation\"\n      ]\n    }\n  },\n  \"criteria_analysis\": [\n    {\n      \"criterion\": \"Awards\",\n      \"achievements\": [\n        \"AI Patent \\u201cWO2021237019A1\\u201d - Environmental Adjustment using AI (Published)\",\n        \"Gartner Data & Analytics Excellence Awards\"\n      ],\n      \"explanation\": \"The candidate has received awards and patents for his work in the field of AI, demonstrating recognition of his excellence in the field.\"\n    },\n    {\n      \"criterion\": \"Membership\",\n      \"achievements\": [],\n      \"explanation\": \"The CV does not provide information about the candidate's membership in associations related to his field.\"\n    },\n    {\n      \"criterion\": \"Press\",\n      \"achievements\": [],\n      \"explanation\": \"There is no evidence of published material about the candidate in professional publications or major media.\"\n    },\n    {\n      \"criterion\": \"Judging\",\n      \"achievements\": [],\n      \"explanation\": \"There is no information about the candidate's participation as a judge of the work of others in his field.\"\n    },\n    {\n      \"criterion\": \"Original Contribution\",\n      \"achievements\": [\n        \"AI Patent \\u201cWO2021237019A1\\u201d - Environmental Adjustment using AI (Published)\",\n        \"Developed and designed an in-house Gen AI Agentic framework for creating AI agents\",\n        \"Fine tuned embedder model (sentence transformer) on custom dataset to improve the search relevancy of user query\",\n        \"Fine tuned open source LLM (7B parameter model) on custom dataset to improve the response time of response model\"\n      ],\n      \"explanation\": \"The candidate has made significant original contributions to AI, including developing AI frameworks and fine tuning models.\"\n    },\n    {\n      \"criterion\": \"Scholarly Articles\",\n      \"achievements\": [],\n      \"explanation\": \"There is no evidence of the candidate's authorship of scholarly articles in the field.\"\n    },\n    {\n      \"criterion\": \"Critical Employment\",\n      \"achievements\": [\n        \"Connectly.AI, San Francisco Bay Area Lead (Founding) AI Engineer\",\n        \"Shopify, San Francisco Bay Area Lead AI/ML Engineer\",\n        \"Twitter, San Francisco Bay Area Lead ML Engineer\",\n        \"View, San Francisco Bay Area Sr ML (Founding) Engineer\",\n        \"VenueNext, San Francisco Bay Area Sr ML (Founding) Engineer\",\n        \"Dailymotion, San Francisco Bay Area ML Engineer\",\n        \"Apple, San Francisco Bay Area Tech Lead\"\n      ],\n      \"explanation\": \"The candidate has been employed in critical roles at reputable organizations, demonstrating his essential capacity in the field.\"\n    },\n    {\n      \"criterion\": \"High Remuneration\",\n      \"achievements\": [],\n      \"explanation\": \"There is no d* Connection #0 to host localhost left intact
irect evidence of high salary or remuneration in the CV.\"\n    }\n  ],\n  \"overall_summary\": \"The candidate convincingly meets 3 out of 8 criteria for the O-1A visa. He has received awards and patents for his work (Awards), made original contributions to his field (Original Contribution), and has been employed in critical roles at reputable organizations (Critical Employment). However, the CV does not provide evidence of the other criteria.\",\n  \"rating\": \"Medium\"\n}"}


## Running with Docker

To run the application using Docker:

1. **Build the Docker image:**
   ```
   docker build -t o1a-visa-analyzer .
   ```

2. **Run the Docker container:**
   ```
   docker run -p 8000:8000 -e OPENAI_API_KEY=your_api_key_here o1a-visa-analyzer
   ```

   The application will be available at `http://localhost:8000`.

## Testing

The `test.ipynb` Jupyter notebook provides a way to test individual components of the application. To use it:

1. Start Jupyter Notebook:
   ```
   poetry run jupyter notebook
   ```

2. Open `test.ipynb` in your browser.

3. Run the cells to test different parts of the application.

## Note

Ensure that you have the necessary permissions and comply with OpenAI's usage policies when using their API. Also, handle CV data responsibly and in compliance with relevant data protection regulations.