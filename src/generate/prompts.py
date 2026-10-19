CV_SUGGESTION_PROMPT = '''
You are a practical career advisor.

Compare the candidate profile with the target job.
Give:
1. Missing or weak skills
2. Weak resume bullet points and improved versions
3. A rewritten professional summary

Use only information present in the candidate profile. Do not invent experience.
Keep the advice specific and concise.

CANDIDATE:
{profile}

TARGET JOB:
{job}
'''
