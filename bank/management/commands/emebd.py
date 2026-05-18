from django.core.management.base import BaseCommand
from bank.models import Entry
from bank.services import embed_text


class Command(BaseCommand):
    help = 'Generate embeddings for all entries'

    def handle(self, *args, **kwargs):
        entries = Entry.objects.filter(embedding=None)
        total = entries.count()

        if total == 0:
            self.stdout.write('No entries need embedding.')
            return

        self.stdout.write(f'Embedding {total} entries...')

        for i, entry in enumerate(entries, 1):
            entry.embedding = embed_text(entry.raw)
            entry.save(update_fields=['embedding'])
            self.stdout.write(f'  [{i}/{total}] {entry.title}')

        self.stdout.write(self.style.SUCCESS(f'\nDone. {total} entries embedded.'))
