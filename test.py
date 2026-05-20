import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bank.services import embed_text
from bank.models import Entry
from pgvector.django import CosineDistance

query_vector = embed_text("Looking for a backend engineer with Django and payments experience")

results = Entry.objects.annotate(
    similarity=1 - CosineDistance('embedding', query_vector)
).order_by('-similarity')[:4]

for r in results:
    print(r.title, r.similarity)