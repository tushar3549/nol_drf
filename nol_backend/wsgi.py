import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE','nol_backend.settings.local')
application=get_wsgi_application()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nol_backend.settings.prod')

application = get_wsgi_application()

# --- Auto-migrate & optional collectstatic on startup (controlled via env) ---
if os.environ.get("DJANGO_AUTO_MIGRATE") == "1":
    try:
        from django.core.management import call_command
        # run migrations (idempotent)
        call_command("migrate", interactive=False)
    except Exception as e:
        # Fail-safe: don't crash the process if migrate fails; log it instead
        print(f"[AUTO-MIGRATE] Error: {e}")

if os.environ.get("DJANGO_AUTO_COLLECTSTATIC") == "1":
    try:
        from django.core.management import call_command
        call_command("collectstatic", interactive=False, verbosity=0, clear=False, link=False, dry_run=False, ignore_patterns=[])
    except Exception as e:
        print(f"[AUTO-COLLECTSTATIC] Error: {e}")
