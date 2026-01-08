import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_almafuerte.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if not username or not password:
    print("⚠️ Variables de superuser no definidas")
else:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✅ Superuser creado")
    else:
        print("ℹ️ Superuser ya existe")
