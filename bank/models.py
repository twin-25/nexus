from django.db import models
import uuid
from pgvector.django import VectorField

# Create your models here.

class Entry(models.Model):
  TYPE_CHOICES = [
    ('project', 'Project'),
    ('experience', 'Work Experience'),
    ('education', 'Education'),
    ('certification', 'Certification'),
    ('achievement', 'Achievement'),
]
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  type = models.CharField(max_length=20, choices=TYPE_CHOICES)
  title = models.CharField(max_length=100)
  organization = models.CharField(max_length=200,null=True, blank=True)
  embedding = VectorField(dimensions=384, null=True, blank=True)
  raw = models.TextField()
  context = models.CharField(max_length=300, blank=True)
  start_date = models.DateField(null=True, blank=True)
  end_date=models.DateField(null=True, blank=True)
  current = models.BooleanField(default=False)
  skills = models.ManyToManyField('Skill', blank=True)
  featured = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.type} - {self.title}"

class Media(models.Model):
  TYPE_CHOICES = [
    ('code', 'Code'),
    ('live', 'Live Demo'),
    ('demo_video', 'Demo Video'),
    ('screenshot', 'Screenshot'),
]
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  entry = models.ForeignKey(Entry, related_name='media', on_delete=models.CASCADE)
  url = models.URLField(blank=True, null=True)
  type = models.CharField(max_length=20, choices=TYPE_CHOICES)
  label = models.CharField(max_length=200, blank=True)

  def __str__(self):
    return f"{self.type} - {self.label}"



class Skill(models.Model):
  CATEGORY_CHOICES = [
    ('language', 'Language'),
    ('framework', 'Framework'),
    ('tool', 'Tool'),
    ('database', 'Database'),
    ('cloud', 'Cloud'),
    ('other', 'Other'),
]
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
  featured = models.BooleanField(default=False)
  icon = models.CharField(max_length=100, blank=True)

  def __str__(self):
    return self.name


class Tag(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  entry = models.ForeignKey(Entry, related_name='tag', on_delete=models.CASCADE)
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name