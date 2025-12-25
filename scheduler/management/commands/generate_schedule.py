from django.core.management.base import BaseCommand
from scheduler.services.scheduler import generate_schedule

class Command(BaseCommand):
    help = "Generate weekly work schedule"

    def handle(self, *args, **kwargs):
        generate_schedule()
        self.stdout.write(self.style.SUCCESS("Schedule generated successfully"))
