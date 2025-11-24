# tasks/admin.py
from django.contrib import admin
from .models import Task  # Task моделин импорттоо


class TaskAdmin(admin.ModelAdmin):
    # Админканын тизмесинде көрүнө турган талаалар
    list_display = (
        'title',
        'status',
        'get_author_username',  # Жаңы кошулган метод
        'created_at'
    )

    # Тизменин үстүнөн чыпкалоо үчүн талаалар
    list_filter = ('status', 'author')

    # Издөө үчүн талаалар
    search_fields = ('title', 'description', 'author__username')

    # Жаңы тапшырма түзүү/өзгөртүү формасындагы талаалардын тартиби
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'full_description', 'status', 'author')
        }),
    )

    # list_display үчүн автордун атын кайтаруучу функция
    # Бул функция Task моделиндеги author талаасын колдонот.
    def get_author_username(self, obj):
        return obj.author.username if obj.author else "Белгисиз"

    get_author_username.short_description = 'Автору'  # Колонканын аталышы


# Task моделин каттоо
admin.site.register(Task, TaskAdmin)