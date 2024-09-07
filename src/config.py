import os

# OpenAI API configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
# OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))

# System message for OpenAI API
SYSTEM_MESSAGE = os.getenv(
    "SYSTEM_MESSAGE", "You are an expert immigration consultant."
)

# Allowed file extensions for CV upload
ALLOWED_FILE_EXTENSIONS = (".pdf", ".docx", ".doc")

# FastAPI server configuration
HOST = "0.0.0.0"
PORT = 8000

# O-1A Visa criteria
O1A_CRITERIA = [
    "Awards",
    "Membership",
    "Press",
    "Judging",
    "Original Contribution",
    "Scholarly Articles",
    "Critical Employment",
    "High Remuneration",
]

# O-1A Visa criteria
O1A_CRITERIA = [
    "Awards",
    "Membership",
    "Press",
    "Judging",
    "Original Contribution",
    "Scholarly Articles",
    "Critical Employment",
    "High Remuneration",
]

# Criteria descriptions
CRITERIA_DESCRIPTIONS = {
    "Awards": "Documentation of the beneficiary's receipt of nationally or internationally recognized prizes or awards for excellence in the field of endeavor.",
    "Membership": "Documentation of the beneficiary's membership in associations in the field for which classification is sought, which require outstanding achievements of their members, as judged by recognized national or international experts in their disciplines or fields.",
    "Press": "Published material in professional or major trade publications or major media about the beneficiary, relating to the beneficiary's work in the field for which classification is sought. This evidence must include the title, date, and author of such published material and any necessary translation.",
    "Judging": "Evidence of the beneficiary's participation on a panel, or individually, as a judge of the work of others in the same or in an allied field of specialization for which classification is sought.",
    "Original Contribution": "Evidence of the beneficiary's original scientific, scholarly, or business-related contributions of major significance in the field.",
    "Scholarly Articles": "Evidence of the beneficiary's authorship of scholarly articles in the field, in professional journals, or other major media.",
    "Critical Employment": "Evidence that the beneficiary has been employed in a critical or essential capacity for organizations and establishments that have a distinguished reputation.",
    "High Remuneration": "Evidence that the beneficiary has either commanded a high salary or will command a high salary or other remuneration for services as evidenced by contracts or other reliable evidence.",
}


# Rating scale
RATING_SCALE = {
    "Low": "Meets 0-2 criteria convincingly",
    "Medium": "Meets 3-4 criteria convincingly",
    "High": "Meets 5 or more criteria convincingly",
}
