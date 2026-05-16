from django.core.management.base import BaseCommand
from bank.models import Entry, Skill
from datetime import date


class Command(BaseCommand):
    help = 'Seed project entries into the database'

    def handle(self, *args, **kwargs):

        entries = [
            {
                'type': 'project',
                'title': 'Ecomora',
                'organization': '',
                'context': 'Best for e-commerce, retail, full-stack, or deployment roles',
                'featured': True,
                'current': False,
                'start_date': date(2024, 10, 1),
                'end_date': date(2024, 12, 1),
                'skills': [
                    'Python', 'Django', 'Django REST Framework', 'SimpleJWT',
                    'PostgreSQL', 'React', 'Redux Toolkit', 'React Router',
                    'Vite', 'Cloudinary', 'Railway', 'Vercel', 'Gunicorn',
                    'Whitenoise', 'PayPal SDK',
                ],
                'raw': """PROJECT: ECOMORA (E-commerce Storefront)
Built a full-stack e-commerce app with product browsing, cart, checkout, order tracking, and admin management. Django REST backend, React + Vite frontend, deployed to Railway.
Tech Stack: Django 5.2.9, DRF 3.16.1, SimpleJWT 5.5.1, django-cors-headers, django-countries, cloudinary-storage, psycopg2, gunicorn, Whitenoise, python-decouple, PostgreSQL; React 19.2.0, Redux Toolkit 2.11.2, React Router 7.10.0, React Bootstrap, Bootswatch, axios 1.13.2, Vite 7.2.2. PayPal SDK present but not wired up.
Models built: Product (explicit _id PK, optional owner User FK, name, image, brand, category, description, rating, numReviews, price, countInStock). Review (FK to Product and User, one review per user per product enforced in view logic, recalculates avg rating and review count on creation). Order (FK to User, paymentMethod, taxPrice, shippingPrice, totalPrice, isPaid, paidAt, isDelivered, deliveredAt). OrderItem (FK to Product and Order, qty, price). ShippingAddress (one-to-one with Order, CountryField via django-countries). Custom JWT serializer injects user metadata into login response. Order creation decrements stock and creates ShippingAddress atomically in the view.
API surface: ~22 endpoints across three groups. Products: list (search + pagination via Django Paginator + name__icontains), top products, detail, create placeholder, update, delete, image upload, create review. Users: login, register, profile read/update, list, delete, get by id, update by id. Orders: list all, create, user's orders, detail, mark paid, mark delivered. All views are function-based with @api_view and explicit permission classes — no routers or viewsets. Root URL config serves React build via TemplateView at /.
Frontend structure: HashRouter SPA with routes for home, product detail, cart (product id + qty as query params), login, register, profile, shipping, payment, place order, order detail, admin user/product/order management. HomePage shows top product carousel when no search is active, keyword + page query params for search and pagination. ProductPage has stock-dependent qty selector and authenticated review submission. PlaceOrderPage computes item/shipping/tax/total client-side before submitting. PaymentPage is a form that saves selected payment method but does not trigger a real PayPal flow.
State management: Redux slices for product list/detail/delete/create/update/review/top, cart, user login/register/details/profile/list/delete/update, order create/details/pay/my-orders/all-orders/deliver. localStorage persistence for userInfo, cartItems, shippingAddress, paymentMethod. Axios wrapped with axios.create using VITE_BACKEND_URL env var; authenticated actions attach Bearer token from Redux state.
Auth flow: SimpleJWT with a custom MyTokenObtainPairView that returns access token plus user fields. Register hashes password, returns token, saves to localStorage. IsAuthenticated for buyer actions, IsAdminUser for admin routes. Logout clears localStorage and resets state slices.
Key integrations: Cloudinary for media uploads via CLOUDINARY_STORAGE. Whitenoise serves React dist folder as static files. django-countries for shipping address country field. PostgreSQL via env vars with SSL required. No websockets or background jobs.
Notable implementation details: Explicit _id PKs on all models align with frontend Redux state keys. Product serializer nests reviews; Order serializer nests order items, shipping address, and user via SerializerMethodField. Backend serves React build from ecomora-frontend/dist and media under /images/. Cart clear on successful order placement.
Challenges and known gaps: Payment is incomplete — PaymentPage only captures method selection, mark-paid endpoint does no gateway verification. Image upload endpoint lacks auth check. Admin create product seeds a placeholder requiring manual update. Checkout has some commented-out validation. CORS is globally open. Railway host hardcoded in ALLOWED_HOSTS.
Deployment status: Deployed to Railway. DEBUG=False, PostgreSQL via env vars, Cloudinary media, React build served through Django. Production static serving configured. Payment and some admin flows are still prototype-level.""",
            },
            {
                'type': 'project',
                'title': 'PennyPilot',
                'organization': '',
                'context': 'Best for fintech, backend, AI integration, payments, or real-time roles',
                'featured': True,
                'current': True,
                'start_date': date(2025, 1, 1),
                'end_date': None,
                'skills': [
                    'Python', 'Django', 'Django REST Framework', 'Django Channels',
                    'SimpleJWT', 'PostgreSQL', 'Redis', 'Stripe', 'Groq SDK',
                    'React', 'Redux Toolkit', 'RTK Query', 'TailwindCSS',
                    'Recharts', 'Railway', 'Vercel', 'Daphne', 'WebSockets',
                ],
                'raw': """PROJECT: PENNYPILOT (AI Personal Finance Tracker)
Built a full-stack personal finance app with transaction management, budgeting, realtime notifications via WebSockets, Stripe subscription upgrades, and an AI financial assistant powered by Groq/Llama.
Tech Stack: Django 6.0.3, DRF 3.17.0, SimpleJWT 5.5.1, Django Channels 4.3.2, Daphne 4.2.1, Stripe Python SDK 15.0.1, Groq 1.1.2 (llama-3.1-8b-instant), django-colorfield, django-cors-headers, python-decouple, SQLite; React 19.2.4, Vite 8.0.1, Tailwind CSS 4.2.2, Redux Toolkit 2.11.2, RTK Query, React Router DOM 7.13.2, jwt-decode 4.0.0, recharts 3.8.1, react-icons, emoji-picker-react.
Models built: Custom User extends AbstractUser with email as login field, unique email, date_of_birth, is_pro flag, ai_usage_count. Category belongs to user or is global (nullable user FK), stores name, icon, color via django-colorfield. Transaction (FK to User and Category, amount, type enum expense/income, mode_of_payment, optional card_type, date, note). Budget (FK to User and Category, limit_amount, month, year, unique_together on user+category+month+year). Notification (FK to User, message, is_read). AIUsageLog (per-user per-feature usage tracking for throttling). Custom JWT serializer adds name, email, is_pro to token claims.
API surface: ~25 HTTP endpoints plus one WebSocket route. Auth: register, login, refresh, profile, profile update. Transactions: list, create, detail, update, delete, categories list, create category, dashboard/summary alias. Budgets: list (filter by month/year), create, update, delete. Notifications: list, mark-as-read, delete. AI: tips, analysis, report (all POST, hitting Groq with tool-calling patterns). Payments: Stripe checkout session create, webhook handler. WebSocket: ws/notifications/ — JWT auth via query string token.
Frontend structure: Landing page, auth pages (login/register), protected pages for dashboard, transactions, budgets, notifications, profile, AI assistant, upgrade flow. PrivateRoutes wrapper checks localStorage token. Dashboard shows balance/income/expense summary cards, category spend pie chart (recharts), recent transactions. TransactionsPage has inline edit/delete and modals for adding transactions and categories. BudgetsPage has month/year selectors and progress bars. AiPage has tabbed UI for tips/analysis/report triggered via RTK Query mutations. Shared Navbar and UI primitives.
State management: Single auth slice storing token, refresh token, decoded JWT payload. RTK Query for all API calls via shared api service with tag-based cache invalidation for categories, transactions, budgets, dashboard, notifications, users. baseQuery globally attaches Bearer token from auth state. localStorage persists token and refresh token.
Auth flow: SimpleJWT. Login returns access + refresh tokens, saved to localStorage, decoded into auth state. PrivateRoutes checks token presence only. Backend uses IsAuthenticated. WebSocket auth resolves user from JWT query string token in Channels consumer.
Key integrations: Stripe Checkout sessions for is_pro upgrades, webhook sets user.is_pro. Groq AI with tool-calling — backend defines tools for transaction/budget lookups and orchestrates tool execution before returning AI response. Django Channels with InMemoryChannelLayer for realtime notifications. Budget spent totals and percentages computed at runtime from transactions.
Notable implementation details: Transaction serializer uses write-only category_id on input, returns nested category object on read. Budget enrichment (spent amount, percentage) happens in view code not the model. Dashboard is a URL alias within the transactions URLconf. AI endpoints structured around multi-action tool-calling pattern with separate system prompts per action type.
Challenges and known gaps: DEBUG=True, CORS_ALLOW_ALL_ORIGINS=True, ALLOWED_HOSTS=[] — all dev config. Frontend auth only checks token existence, not expiration. Stripe success/cancel URLs hardcoded to localhost. AI usage throttling exists in model but not enforced in active endpoints. InMemoryChannelLayer not scalable.
Deployment status: Deployed to Railway (backend) and Vercel (frontend). Resolved a series of real deployment challenges: migrated Cloudinary config to Django 5.2 STORAGES dict format, configured Neon PostgreSQL, bundled React build for production, set up Whitenoise for static files.""",
            },
            {
                'type': 'project',
                'title': 'Ascend',
                'organization': '',
                'context': 'Best for productivity tools, AI assistant, full-stack, or frontend-heavy roles',
                'featured': True,
                'current': False,
                'start_date': date(2024, 7, 1),
                'end_date': date(2024, 9, 1),
                'skills': [
                    'Python', 'Django', 'Django REST Framework', 'SimpleJWT',
                    'React', 'Redux Toolkit', 'RTK Query', 'React Router',
                    'Vite', 'Anthropic Claude',
                ],
                'raw': """PROJECT: ASCEND (Task Management + AI Productivity App)
Built a full-stack task management app called Ascend with an AI assistant named Alto. Django REST Framework backend, React + Vite frontend, Redux Toolkit with RTK Query for state and API management.
Tech Stack: Django 6, DRF, SimpleJWT, SQLite, Anthropic API (Claude Haiku 4.5), React 19, Vite 7, Redux Toolkit 2 + RTK Query, React Router DOM 7, Material-UI 7, React Bootstrap, React Big Calendar, Three.js (Vanta Birds animation), SASS, date-fns, react-markdown, python-decouple, django-cors-headers, django-colorfield.
Models built: Custom AbstractUser (email uniqueness enforced), Task (with category enum Work/Personal/Others, due date, ManyToMany tags), Subtask (nested under Task), Tag (max 10 per user, custom hex color via django-colorfield), StickyNote (custom color), CalendarEvent (start + optional end datetime).
API surface: 28+ endpoints. Auth: register, login (email OR username supported), token refresh. Tasks: full CRUD + dedicated today/tomorrow/thisweek filter endpoints. Tags: list, create, delete (limit enforced in view). StickyNotes: full CRUD. CalendarEvents: full CRUD. Chatbot: single POST endpoint that feeds user context to Claude.
Frontend pages: Welcome (Vanta Birds 3D animated background), Register, Login, Home dashboard (Today/Tomorrow/Week task sections side by side), Day (today's tasks detailed), Calendar (React Big Calendar with click-to-create events), Sticky Wall.
Redux/RTK Query setup: Single store with 6 separate API slices — userApi, taskApi, tagApi, stickyNoteApi, calendarEventApi, chatbotApi. Auto-generated hooks for all operations. RTK Query caching reduces redundant API calls across components.
Auth flow: JWT stored in localStorage, PrivateRoutes component guards protected pages, all API requests attach Bearer token via RTK Query baseQuery config. Access token lifetime 10 days.
AI integration (Alto): Backend view serializes user's full context (tasks, tags, events, notes) and sends it to Claude Haiku with a productivity-focused system prompt. Prompt caching enabled. Last 10 messages of conversation history maintained. Features: task prioritization suggestions, pattern recognition, motivational messages, event reminders.
Notable implementation details: Tag limit enforced in view logic. Calendar events created by clicking empty slots in React Big Calendar. Sidebar dynamically shows task counts broken down by category. Color fields use django-colorfield for clean hex storage. Subtask model exists but no endpoints or UI built for it — intentionally deferred.
Challenges/known gaps: DEBUG=True and ALLOWED_HOSTS=[] left for dev convenience. No token invalidation on logout. No pagination. Error states not displayed in UI in several components.
Deployment status: Not deployed. SQLite used throughout. Foundation laid for future features: notifications, search/filtering, subtask UI, dark mode, profile management, data export.""",
            },
        ]

        created_count = 0
        for entry_data in entries:
            skills = entry_data.pop('skills')
            entry, created = Entry.objects.get_or_create(
                title=entry_data['title'],
                defaults=entry_data
            )
            if created:
                # attach skills
                for skill_name in skills:
                    try:
                        skill = Skill.objects.get(name=skill_name)
                        entry.skills.add(skill)
                    except Skill.DoesNotExist:
                        self.stdout.write(f"  skill not found: {skill_name}")
                created_count += 1
                self.stdout.write(f"  created: {entry_data['title']}")
            else:
                self.stdout.write(f"  skipped: {entry_data['title']} (already exists)")

        self.stdout.write(self.style.SUCCESS(f'\nDone. {created_count} entries created.'))