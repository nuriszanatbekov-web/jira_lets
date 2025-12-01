# tasks/admin.py

from django.contrib import admin
from .models import Task


# Task моделин Admin панелинде кантип көрсөтүү керек
class TaskAdmin(admin.ModelAdmin):
    # Тизмеде көрсөтүлө турган талаалар
    list_display = ('title', 'status', 'get_assigned_to', 'author', 'created_at')

    # Тизмени чыпкалоо үчүн талаалар
    list_filter = ('status', 'assigned_to', 'created_at')

    # Тизмени издөө үчүн талаалар
    search_fields = ('title', 'description')

    # Редактирлөө барагындагы талаалардын тартиби
    fieldsets = (
        (None, {'fields': ('title', 'description', 'full_description', 'status')}),
        ('Дайындоо', {'fields': ('author', 'assigned_to')}),
    )

    # ManyToMany талааларын (assigned_to) жакшыраак көрсөтүү
    filter_horizontal = ('assigned_to',)

    # 'assigned_to' талаасынын аттарын тизмеде көрсөтүүчү функция
    def get_assigned_to(self, obj):
        # Бардык дайындалгандарды запятая менен бөлүп кайтарат
        return ", ".join([user.username for user in obj.assigned_to.all()])

    get_assigned_to.short_description = 'Дайындалгандар'  # Колонканын атын кыргызча кылуу


# Жаңы TaskAdmin классын каттайбыз
admin.site.register(Task, TaskAdmin)