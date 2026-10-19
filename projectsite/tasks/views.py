from django.shortcuts import render, redirect
from django.db.models import Q, Case, When, Value, IntegerField, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Task, Note, SubTask, Category, Priority, Profile
from .forms import TaskForm, NoteForm, SubTaskForm, CategoryForm, PriorityForm, ProfileForm

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

    def get_queryset(self):
        qs = super().get_queryset().select_related("priority", "category")

        # search
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        # custom ranks so the order follows meaning, not the alphabet
        qs = qs.annotate(
            status_rank=Case(
                When(status="Pending", then=Value(0)),
                When(status="In Progress", then=Value(1)),
                When(status="Completed", then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            ),
            priority_rank=Case(
                When(priority__name="Critical", then=Value(0)),
                When(priority__name="High", then=Value(1)),
                When(priority__name="Medium", then=Value(2)),
                When(priority__name="Low", then=Value(3)),
                When(priority__name="Optional", then=Value(4)),
                default=Value(5),
                output_field=IntegerField(),
            ),
        )

        soonest = F("deadline").asc(nulls_last=True)
        sort_by = self.request.GET.get("sort_by", "deadline")

        if sort_by == "title":
            return qs.order_by("title", "id")
        if sort_by == "status":
            return qs.order_by("status_rank", soonest, "id")
        if sort_by == "priority":
            return qs.order_by("priority_rank", soonest, "id")
        if sort_by == "category":
            return qs.order_by("category__name", soonest, "id")
        return qs.order_by(soonest, "id")   # deadline (default)


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

# ---------- Profile ----------
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if not profile.display_name:
        profile.display_name = (
            request.user.get_full_name() or request.user.username
        )

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile.html", {
        "form": form,
        "profile": profile,
    })