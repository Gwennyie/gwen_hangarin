from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from tasks.models import Priority, Category, Task, Note, SubTask

STATUSES = ["Pending", "In Progress", "Completed"]


class Command(BaseCommand):
    help = "Create initial data for the application"

    def handle(self, *args, **kwargs):
        self.create_tasks(20)

    def create_tasks(self, count):
        fake = Faker()
        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        for _ in range(count):
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
            "Initial data for tasks created successfully."))
