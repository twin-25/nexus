import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bank.tools import analyze_jd

jd = """
We are looking for a Backend Engineer with 2+ years of experience.
Must have Django, PostgreSQL, and REST API experience.
Nice to have: Redis, Docker, AWS.
You will be working on our fintech platform handling payments and transactions.
"""

result = analyze_jd(jd)
print(result)