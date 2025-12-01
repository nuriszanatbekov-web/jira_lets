from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task, Team  # ⭐ Team моделин импорттоо
from .forms import TaskForm  # TeamForm'ду кийинчерээк импорттойбуз
from django.views.decorators.http import require_POST
from django.utils import timezone  # Убакытты форматтоо үчүн
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Профиль үчүн User моделин импорттоо

# --- API ҮЧҮН ИМПОРТТОР ---
from rest_framework import viewsets, permissions
from .serializers import TaskSerializer


# --- КАНБАН ТАКТАСЫ (Көпчүлүк логикаңызды сактадык) ---
# @login_required
def kanban_board(request):
    # --- AJAX (Жаңы Тапшырма Кошуу) Логикасы ---
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.author = request.user
            task.save()
            form.save_m2m()  # ManyToMany талааларын сактоо

            formatted_created_at = timezone.localtime(task.created_at).strftime("%b %d, %H:%M")
            author_username = task.author.username if task.author else "(Белгисиз)"
            assignee_usernames = [user.username for user in task.assigned_to.all()]

            return JsonResponse({
                "success": True,
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "full_description": task.full_description,
                "status": task.status,
                "author_username": author_username,
                "assignee_usernames": assignee_usernames,
                "created_at": formatted_created_at,
                "csrf_token": request.META.get('CSRF_COOKIE', '')
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    # --- ЖАЛПЫ КАНБАН ТАКТАСЫН КӨРСӨТҮҮ ЛОГИКАСЫ (GET) ---
    form = TaskForm()
    all_tasks = Task.objects.all().select_related('author').prefetch_related('assigned_to').order_by('-created_at')

    context = {
        'todo_tasks': all_tasks.filter(status='TODO'),
        'progress_tasks': all_tasks.filter(status='IN_PROGRESS'),
        'done_tasks': all_tasks.filter(status='DONE'),
        'form': form,
    }
    return render(request, "tasks/kanban_board.html", context)


# --- СТАТУС ЖАНА ӨЧҮРҮҮ (Өзгөртүүлөр жок) ---
@require_POST
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get('new_status')

    if new_status in [choice[0] for choice in Task.STATUS_CHOICES]:
        task.status = new_status
        task.save()
        return JsonResponse({"success": True, "new_status": new_status, "id": task_id})

    return JsonResponse({"success": False, "error": "Туура эмес статус берилди."}, status=400)


@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"success": True, "id": task_id})
    return redirect('kanban_board')


# --- ⭐ ПРОФИЛЬ VIEW'УН ТОЛУКТОО ---
@login_required  # Профильге кирүү үчүн авторизация талап кылынат
def user_profile(request):
    """Колдонуучунун профили жана статистикасы."""
    user = request.user

    # Колдонуучу түзгөн тапшырмалардын саны (Task моделинде related_name='created_tasks')
    created_task_count = user.created_tasks.count()

    context = {
        'page_title': 'Менин Профилим',
        'user': user,
        'created_task_count': created_task_count,
        # 'teams': user.teams.all(), # Колдонуучу кирген командалар
        # 'profile_form': UserUpdateForm(instance=user) # Форманы кийин кошобуз
    }
    # tasks/user_profile.html шаблонун колдонуу (мурунку жоопто сунушталган)
    return render(request, 'tasks/user_profile.html', context)


# --- ⭐ КОМАНДАЛАР VIEW'УН ТОЛУКТОО ---
# @login_required # Эгер авторизация керек болсо
def teams_list(request):
    """Командалардын тизмесин көрсөтүү."""

    # Бардык командаларды жана алардын мүчөлөрүн алдын ала жүктөө
    teams = Team.objects.all().prefetch_related('members')

    # Эгерде кийинчерээк форма кошулса, бул жерде TeamForm() болот

    context = {
        'page_title': 'Командалар',
        'teams': teams,
        # 'form': TeamForm(),
    }
    # tasks/teams_list.html шаблонун колдонуу (мурунку жоопто сунушталган)
    return render(request, 'tasks/teams_list.html', context)


# --- API VIEWS (DRF) (Өзгөртүүлөр жок) ---
class TaskViewSet(viewsets.ModelViewSet):
    """
    Task модели үчүн CRUD (түзүү, окуу, өзгөртүү, өчүрүү) API endpoint'и.
    """
    queryset = Task.objects.all().select_related('author').prefetch_related('assigned_to').order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()