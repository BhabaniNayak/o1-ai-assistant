import io
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from docx import Document
import os
import re
import json
from typing import List
from pydantic import BaseModel
from src.config import O1A_CRITERIA, CRITERIA_DESCRIPTIONS, RATING_SCALE
import logging

logger = logging.getLogger(__name__)


class CriterionAnalysis(BaseModel):
    criterion: str
    achievements: List[str]
    explanation: str


class OutputSchema(BaseModel):
    criteria_analysis: List[CriterionAnalysis]
    overall_summary: str
    rating: str


class Utilities(BaseModel):
    def read_cv(self, file_path: str) -> str:
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() == ".pdf":
            try:
                output_string = io.StringIO()
                with open(file_path, "rb") as fin:
                    extract_text_to_fp(
                        fin,
                        output_string,
                        laparams=LAParams(),
                        output_type="text",
                        codec="utf-8",
                    )
                text = output_string.getvalue()
                # logger.info(f"Total extracted text length: {len(text)}")
            except Exception as e:
                logger.error(f"Error reading PDF: {str(e)}")
                raise

        elif file_extension.lower() in [".docx", ".doc"]:
            try:
                doc = Document(file_path)
                text = " ".join(paragraph.text for paragraph in doc.paragraphs)
                # logger.info(f"Extracted text length from Word document: {len(text)}")
            except Exception as e:
                logger.error(f"Error reading Word document: {str(e)}")
                raise

        else:
            raise ValueError("Unsupported file format")

        # Clean up the text
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\n+", "\n", text)
        text = text.strip()

        # logger.info(f"Cleaned text length: {len(text)}")
        # logger.info(f"First 100 characters of cleaned text: {text[:100]}")

        return text

    def generate_prompt(self, cv_text: str) -> str:
        criteria_xml = "\n".join(
            f"<{criterion}>{CRITERIA_DESCRIPTIONS[criterion]}</{criterion}>"
            for criterion in O1A_CRITERIA
        )
        rating_scale = "\n".join(
            f"- {rating}: {description}" for rating, description in RATING_SCALE.items()
        )

        prompt = f"""
        You are an immigration expert evaluating candidates for O-1A Visa eligibility. An O-1A visa is granted to individuals with extraordinary ability in sciences, education, business, or athletics (excluding arts, motion pictures, or television industry).

        Given a candidate's CV and 8 criteria, your tasks are:
        1) Match the candidate's achievements to each of the 8 O-1A criteria.
        2) Rate the candidate's overall chances of O-1A visa qualification.

        For each criterion, provide:
        - Relevant achievements from the CV
        - A brief explanation of how these achievements relate to the criterion

        Use the following rating scale:
        {rating_scale}

        Output your analysis in this JSON structure:
        {OutputSchema.model_json_schema() if hasattr(OutputSchema, 'model_json_schema') else OutputSchema.schema()}

        The 8 criteria are:
        <Criterions>
        {criteria_xml}
        </Criterions>

        Candidate's CV:
        <candidate_cv>
        {cv_text}
        </candidate_cv>

        Analyze the CV thoroughly and provide your evaluation based on these criteria.
        """
        return prompt.strip()

    def parse_and_format_output(self, result: str) -> str:
        try:
            # Parse the JSON string into a Python dictionary
            data = json.loads(result)

            # Check if the expected structure is present
            if "analysis" in data:
                # The actual content is inside the "analysis" key
                content = json.loads(data["analysis"].split("Raw content:\n", 1)[1])

                criteria_analysis = content.get("criteria_analysis", [])
                overall_summary = content.get(
                    "overall_summary", "No overall summary provided."
                )
                rating = content.get("rating", "No rating provided.")

                # Format the output
                formatted_output = f"Overall Summary: {overall_summary}\n\n"
                formatted_output += f"Rating: {rating}\n\n"
                formatted_output += "Criteria Analysis:\n"

                for criterion in criteria_analysis:
                    formatted_output += f"- {criterion['criterion']}:\n"
                    formatted_output += f"  Explanation: {criterion['explanation']}\n"
                    if criterion["achievements"]:
                        formatted_output += "  Achievements:\n"
                        for achievement in criterion["achievements"]:
                            formatted_output += f"    - {achievement}\n"
                    formatted_output += "\n"

                return formatted_output
            else:
                # If the structure doesn't match, return the raw content
                return f"Raw content:\n{json.dumps(data, indent=2)}"
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response\n\nRaw content:\n{result}"
        except KeyError as e:
            return f"Error: Missing expected key in data structure: {str(e)}\n\nRaw content:\n{result}"
        except Exception as e:
            return f"Error: {str(e)}\n\nRaw content:\n{result}"
