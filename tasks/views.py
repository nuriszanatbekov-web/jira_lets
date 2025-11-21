from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm
from django.views.decorators.http import require_POST


def kanban_board(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return JsonResponse({
                "success": True,
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status
            })
        else:
            return JsonResponse({"success": False})

    form = TaskForm()
    context = {
        'todo_tasks': Task.objects.filter(status='TODO').order_by('-created_at'),
        'progress_tasks': Task.objects.filter(status='IN_PROGRESS').order_by('-created_at'),
        'done_tasks': Task.objects.filter(status='DONE').order_by('-created_at'),
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
