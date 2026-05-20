from sentence_transformers import SentenceTransformer
from pgvector.django import CosineDistance
from .models import Entry

model = SentenceTransformer('all-MiniLM-L6-v2')

TOP_K = 4
THRESHOLD = 0.3

def embed_text(text):

  embedding = model.encode(text)
  return embedding

def search_bank(query):

  query_vector = embed_text(query)

  return Entry.objects.annotate(
      similarity=1 - CosineDistance('embedding', query_vector)
  ).filter(
      similarity__gte=THRESHOLD
  ).order_by('-similarity')[:TOP_K]