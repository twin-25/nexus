from .models import Entry, Skill
import os
from anthropic import Anthropic
import json

client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'))

def get_entry(title):
  try:
    query = Entry.objects.get(title__iexact=title)
    return query
  except Entry.DoesNotExist:
    return {'error':'No entries found with the given title'}
  

def get_skills():
  return Skill.objects.all()

def analyze_jd(job_description):

  response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=1024,
    system = """
    You are a resume analyzing specialist. Extract role, seniority, domain, required_skills, nice_to_have, and keywords from the job description.

    Return ONLY a JSON object with no markdown, no code blocks, no explanation. Just raw JSON.
{
    "role": "Backend Engineer",
    "seniority": "mid-level",
    "domain": "fintech",
    "required_skills": ["Django", "PostgreSQL", "REST APIs"],
    "nice_to_have": ["Redis", "Docker"],
    "keywords": ["payments", "scalability", "microservices"]
}

""",
    messages=[
        {
            "role": "user",
            "content": job_description,
        }
    ],

)
  result = response.content[0].text.strip()
  result = result.replace('```json', '').replace('```', '').strip()
  return json.loads(result)


def draft_section(entries, job_description, section):
    entries_text = "\n\n".join([f"Title: {e['title']}\nDetails: {e['raw']}" for e in entries])
    
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system="""You are a professional resume writer. Based on the provided job description and candidate experience, write the requested section of the resume.

Requirements:
- Must pass ATS filters by naturally including keywords from the job description
- Must read well to human recruiters
- Each bullet follows: Action Verb + What You Did + Result/Impact
- Maximum 4 bullet points per entry
- Return only the bullet points, no explanations, no headers, no extra text""",
        messages=[
            {
                "role": "user",
                "content": f"Job Description:\n{job_description}\n\nCandidate Experience:\n{entries_text}\n\nSection to write: {section}"
            }
        ],
    )
    return response.content[0].text.strip()


def score_match(jd, draft):
    entries_text = "\n\n".join([f"Title: {e.title}\nDetails: {e.raw}" for e in entries])
    
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system="""You are a Senior recruting engineer. Based on the provided job description and candidate experience draft, score the resume on a sclae of 100

    Requirements:
    - Must pass ATS filters by naturally including keywords from the job description
    - Must read well to human recruiters
    - Each bullet follows: Action Verb + What You Did + Result/Impact
    - Maximum 4 bullet points per entry
    - Return only the bullet points, no explanations, no headers, no extra text""",
        messages=[
            {
                "role": "user",
                "content": f"Job Description:\n{job_description}\n\nCandidate Experience draft:\n{entries_text}\n\nSection to write: {section}"
            }
        ],
    )
    return response.content[0].text.strip()

def score_match(jd, draft):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system="""You are a senior software engineer and resume expert. Compare the candidate's experience against the job description and score the match from 0-100 where 100 is a perfect match.

        Evaluate based on:
        - Relevant skills and technologies
        - Domain experience match
        - Seniority level match
        - Keyword presence

        Return ONLY raw JSON in this format:
        {
            "score": 85,
            "strengths": ["strength 1", "strength 2"],
            "gaps": ["gap 1", "gap 2"],
            "verdict": "Strong match for this role"
        }
        No markdown, no code blocks, start with { and end with }.""",
        messages=[
            {
                "role": "user",
                "content": f"Job Description:\n{jd}\n\nCandidate Resume Draft:\n{draft}"
            }
        ],
    )
    result = response.content[0].text.strip()
    result = result.replace('```json', '').replace('```', '').strip()
    return json.loads(result)
  
  





  

