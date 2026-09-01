from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create/update the shared service account the dashboard logs in as for write access."

    def handle(self, *args, **options):
        username = settings.DASHBOARD_USERNAME
        password = settings.DASHBOARD_PASSWORD
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"is_staff": True},
        )
        user.set_password(password)
        user.is_staff = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f"Dashboard user '{username}' {'created' if created else 'updated'}.")
        )
