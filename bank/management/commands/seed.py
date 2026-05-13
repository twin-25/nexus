from django.core.management.base import BaseCommand
from bank.models import Skill


class Command(BaseCommand):
    help = 'Seed skills into the database'

    def handle(self, *args, **kwargs):
        skills = [
            # Languages
            {'name': 'Python', 'category': 'language', 'featured': True, 'icon': 'python'},
            {'name': 'JavaScript', 'category': 'language', 'featured': True, 'icon': 'javascript'},
            {'name': 'SQL', 'category': 'language', 'featured': True, 'icon': ''},
            {'name': 'HTML/CSS', 'category': 'language', 'featured': True, 'icon': 'html5'},
            {'name': 'Java', 'category': 'language', 'featured': True, 'icon': 'java'},
            {'name': 'C', 'category': 'language', 'featured': True, 'icon': 'c'},

            # Frontend
            {'name': 'React', 'category': 'framework', 'featured': True, 'icon': 'react'},
            {'name': 'Redux Toolkit', 'category': 'framework', 'featured': True, 'icon': 'redux'},
            {'name': 'RTK Query', 'category': 'framework', 'featured': False, 'icon': ''},
            {'name': 'React Router', 'category': 'framework', 'featured': False, 'icon': 'reactrouter'},
            {'name': 'TailwindCSS', 'category': 'framework', 'featured': True, 'icon': 'tailwindcss'},
            {'name': 'Recharts', 'category': 'framework', 'featured': False, 'icon': ''},

            # Backend
            {'name': 'Django', 'category': 'framework', 'featured': True, 'icon': 'django'},
            {'name': 'Django REST Framework', 'category': 'framework', 'featured': False, 'icon': 'django'},
            {'name': 'Django Channels', 'category': 'framework', 'featured': False, 'icon': 'django'},
            {'name': 'Flask', 'category': 'framework', 'featured': True, 'icon': 'flask'},
            {'name': 'SimpleJWT', 'category': 'framework', 'featured': False, 'icon': ''},

            # Databases
            {'name': 'PostgreSQL', 'category': 'database', 'featured': True, 'icon': 'postgresql'},
            {'name': 'SQLite', 'category': 'database', 'featured': True, 'icon': 'sqlite'},

            # AI/ML
            {'name': 'Groq SDK', 'category': 'tool', 'featured': False, 'icon': ''},
            {'name': 'Anthropic Claude', 'category': 'tool', 'featured': False, 'icon': ''},

            # DevOps & Cloud
            {'name': 'Docker', 'category': 'cloud', 'featured': True, 'icon': 'docker'},
            {'name': 'AWS EC2', 'category': 'cloud', 'featured': True, 'icon': 'amazonwebservices'},
            {'name': 'AWS S3', 'category': 'cloud', 'featured': False, 'icon': 'amazonwebservices'},
            {'name': 'Railway', 'category': 'cloud', 'featured': False, 'icon': ''},
            {'name': 'Vercel', 'category': 'cloud', 'featured': False, 'icon': 'vercel'},
            {'name': 'Gunicorn', 'category': 'tool', 'featured': False, 'icon': ''},
            {'name': 'Daphne', 'category': 'tool', 'featured': False, 'icon': ''},
            {'name': 'Redis', 'category': 'tool', 'featured': False, 'icon': 'redis'},

            # Payments & APIs
            {'name': 'Stripe', 'category': 'tool', 'featured': True, 'icon': 'stripe'},
            {'name': 'PayPal SDK', 'category': 'tool', 'featured': False, 'icon': ''},
            {'name': 'Cloudinary', 'category': 'tool', 'featured': False, 'icon': 'cloudinary'},
            {'name': 'WebSockets', 'category': 'tool', 'featured': False, 'icon': ''},

            # Tools
            {'name': 'Git', 'category': 'tool', 'featured': True, 'icon': 'git'},
            {'name': 'GitHub', 'category': 'tool', 'featured': False, 'icon': 'github'},
            {'name': 'VS Code', 'category': 'tool', 'featured': True, 'icon': 'vscode'},
            {'name': 'Vite', 'category': 'tool', 'featured': False, 'icon': 'vitejs'},
            {'name': 'ESLint', 'category': 'tool', 'featured': False, 'icon': 'eslint'},
            {'name': 'Linux Shell', 'category': 'tool', 'featured': False, 'icon': 'linux'},
        ]

        created_count = 0
        for skill_data in skills:
            _, created = Skill.objects.get_or_create(
                name=skill_data['name'],
                defaults={
                    'category': skill_data['category'],
                    'featured': skill_data['featured'],
                    'icon': skill_data['icon'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"  created: {skill_data['name']}")
            else:
                self.stdout.write(f"  skipped: {skill_data['name']} (already exists)")

        self.stdout.write(self.style.SUCCESS(f'\nDone. {created_count} skills created.'))