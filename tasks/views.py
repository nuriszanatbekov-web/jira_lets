from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm
from django.views.decorators.http import require_POST
from rest_framework import viewsets, permissions
from .serializers import TaskSerializer


# --- ЖАҢЫ КОШУЛДУ: API ҮЧҮН ИМПОРТТОР АЯКТАДЫ ---


# Эгер колдонуучу авторизацияланган болсо, функцияны 'login_required' менен коргоңуз.
# Эгер сиз азырынча login_required колдонбосоңуз, бул сапты комментарийде калтырсаңыз болот.
# @login_required
def kanban_board(request):
    # --- AJAX (Жаңы Тапшырма Кошуу) Логикасы ---
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)

            # 1. АВТОРДУ САКТОО (Эгер колдонуучу авторизацияланган болсо)
            if request.user.is_authenticated:
                task.author = request.user

            task.save()

            # 2. JSON ЖООБУНА АВТОРДУН АТЫН КОШУУ
            author_username = task.author.username if task.author else "(Белгисиз)"

            return JsonResponse({
                "success": True,
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "author_username": author_username  # Жаңы кошулду
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors})

    # --- ЖАЛПЫ КАНБАН ТАКТАСЫН КӨРСӨТҮҮ ЛОГИКАСЫ (GET) ---
    form = TaskForm()

    # АВТОРДУН АТЫН БАЗАДАН БИР ЧАКЫРУУ МЕНЕН АЛУУ
    # 'select_related('author')' колдонулат
    all_tasks = Task.objects.all().select_related('author').order_by('-created_at')

    context = {
        'todo_tasks': all_tasks.filter(status='TODO'),
        'progress_tasks': all_tasks.filter(status='IN_PROGRESS'),
        'done_tasks': all_tasks.filter(status='DONE'),
        'form': form,
    }
    return render(request, "tasks/kanban_board.html", context)


@require_POST
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get('new_status')
    if new_status in [choice[0] for choice in Task.STATUS_CHOICES]:
        task.status = new_status
        task.save()
    return redirect('kanban_board')


@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "id": task_id})
    return redirect('kanban_board')


# --- ЖАҢЫ КОШУЛДУ: API VIEWS (DRF) ---
class TaskViewSet(viewsets.ModelViewSet):
    """
    Task модели үчүн CRUD (түзүү, окуу, өзгөртүү, өчүрүү) API endpoint'и.
    """
    # Маалыматтарды алууда авторду кошо алгыла (Оптимизация)
    queryset = Task.objects.all().select_related('author').order_by('-created_at')
    serializer_class = TaskSerializer

    # API'ге кирүү уруксаттары: Кирген колдонуучулар окуй жана өзгөртө алат.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Жаңы тапшырма түзүлгөндө, авторду автоматтык түрдө учурдагы колдонуучу кылып орнотуу
    def perform_create(self, serializer):
        # Эгер колдонуучу авторизацияланган болсо, author талаасын учурдагы user кылып коёт
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()
