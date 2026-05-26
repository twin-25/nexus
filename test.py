import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bank.tools import analyze_jd, draft_section, score_match
from bank.services import search_bank

jd = """
We are looking for a Backend Engineer with 2+ years of experience.
Must have Django, PostgreSQL, and REST API experience.
Nice to have: Redis, Docker, AWS.
You will be working on our fintech platform handling payments and transactions.
"""

entries = search_bank(jd)
draft = draft_section(entries, jd, "experience")
score = score_match(jd, draft)
print(score)


