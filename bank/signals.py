from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Entry
from .services import embed_text

@receiver(post_save, sender=Entry)
def generate_embedding(sender, instance, **kwargs):
  if instance.raw and instance.embedding is None:
    instance.embedding = embed_text(instance.raw)

  
