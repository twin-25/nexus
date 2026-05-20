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








  

