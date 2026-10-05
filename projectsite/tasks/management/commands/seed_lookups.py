from django.core.management.base import BaseCommand
from tasks.models import Priority, Category


class Command(BaseCommand):
    help = "Manually add Priority and Category records"

    def handle(self, *args, **options):
        for name in ["High", "Medium", "Low", "Critical", "Optional"]:
            Priority.objects.get_or_create(name=name)

        for name in ["Work", "School", "Personal", "Finance", "Projects"]:
            Category.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("Priorities and categories created."))