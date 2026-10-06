from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Task, Note, SubTask, Category, Priority
from .forms import TaskForm, NoteForm, SubTaskForm, CategoryForm, PriorityForm

class HomePageView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'home'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = Task.objects.count()
        completed = Task.objects.filter(status="Completed").count()
        pending = Task.objects.filter(status="Pending").count()
        in_progress = Task.objects.filter(status="In Progress").count()

        context["total_tasks"] = total
        context["completed_tasks"] = completed
        context["pending_tasks"] = pending
        context["in_progress_tasks"] = in_progress
        context["total_notes"] = Note.objects.count()
        context["total_subtasks"] = SubTask.objects.count()
        context["completion_percentage"] = round((completed / total) * 100) if total else 0

        tasks_with_deadline = Task.objects.exclude(deadline__isnull=True)
        context["tasks_calendar_data"] = [
    {
        "id": t.id,
        "title": t.title,
        "status": t.status,
        "date": t.deadline.strftime("%Y-%m-%d"),
    }
    for t in tasks_with_deadline
]

        return context


# ---------- Task ----------
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task_list.html'
    paginate_by = 5
    ordering = ["status", "deadline"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return qs


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')


# ---------- Note ----------
class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'note_list.html'
    paginate_by = 5
    ordering = ["task__title", "-created_at"]

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(content__icontains=query))
        return qs


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_del.html'
    success_url = reverse_lazy('note-list')


# ---------- SubTask ----------
class SubTaskList(LoginRequiredMixin, ListView):
    model = SubTask
    context_object_name = 'subtasks'
    template_name = 'subtask_list.html'
    paginate_by = 5

    def get_ordering(self):
        allowed = ["title", "parent_task__title", "status"]
        sort_by = self.request.GET.get("sort_by")
        if sort_by in allowed:
            return sort_by
        return "title"

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(parent_task__title__icontains=query)
            )
        return qs


class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')


class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'subtask_del.html'
    success_url = reverse_lazy('subtask-list')


# ---------- Category ----------
class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category_del.html'
    success_url = reverse_lazy('category-list')


# ---------- Priority ----------
class PriorityList(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = 'priorities'
    template_name = 'priority_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(Q(name__icontains=query))
        return qs


class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')


class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = 'priority_del.html'
    success_url = reverse_lazy('priority-list')