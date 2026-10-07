from django.forms import ModelForm
from django import forms
from .models import Task, Note, SubTask, Category, Priority


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = "__all__"


class SubTaskForm(ModelForm):
    class Meta:
        model = SubTask
        fields = "__all__"


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class PriorityForm(ModelForm):
    class Meta:
        model = Priority
        fields = "__all__"