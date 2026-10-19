import re

ALLOWED_TOPICS = [
    "career", "resume", "cv", "job", "jobs", "interview", "skill",
    "skills", "employment", "developer", "data", "education", "role",
    "salary", "application", "work", "internship", "python", "java",
    "sql", "programming", "machine learning", "software", "analytics"
]

BLOCKED_PATTERNS = [
    r"ignore (all|any|the) previous instructions",
    r"jailbreak",
    r"how to make a bomb",
    r"malware",
    r"steal passwords",
]

def validate_input(text: str) -> tuple[bool, str]:
    text = text.strip()
    if not text:
        return False, "Please enter a question."

    lower = text.lower()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, lower):
            return False, "I can only help with safe career-related questions."

    if not any(topic in lower for topic in ALLOWED_TOPICS):
        return False, "This mentor is limited to career, resume, job, skills, and interview topics."

    return True, ""
