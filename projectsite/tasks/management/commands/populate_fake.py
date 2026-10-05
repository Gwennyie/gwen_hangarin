from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tasks.models import Priority, Category, Task, Note, SubTask

STATUSES = ["Pending", "In Progress", "Completed"]


class Command(BaseCommand):
    help = "Generate fake Task, Note, and SubTask data using Faker"

    def add_arguments(self, parser):
        parser.add_argument("count", nargs="?", type=int, default=10)

    def handle(self, *args, **options):
        fake = Faker()
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities or not categories:
            self.stderr.write("Run `python manage.py seed_lookups` first.")
            return

        for _ in range(options["count"]):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=fake.random_element(elements=STATUSES),
                category=fake.random_element(elements=categories),
                priority=fake.random_element(elements=priorities),
            )

            Note.objects.create(
                task=task,
                content=fake.paragraph(nb_sentences=2),
            )

            for _ in range(fake.random_int(min=1, max=3)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=STATUSES),
                )

        self.stdout.write(self.style.SUCCESS(
            f"Created {options['count']} tasks with notes and subtasks."
        ))