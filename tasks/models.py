# tasks/models.py

from django.db import models
from django.contrib.auth.models import User  # Django'нун User моделин импорттоо


class Task(models.Model):
    # Статустардын тандоосу
    STATUS_CHOICES = [
        ('TODO', 'Todo'),
        ('IN_PROGRESS', 'Progress'),
        ('DONE', 'Done')
    ]

    # Негизги маалыматтар
    title = models.CharField(max_length=200, verbose_name='Аты')
    description = models.CharField(max_length=200, verbose_name='Кыскача Баяндама')
    full_description = models.TextField(blank=True, null=True, verbose_name='Толук Баяндама')

    # Статус
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO', verbose_name='Статусу')

    # 🌟 АВТОР (Foreign Key - Бир Колдонуучу)
    # Тапшырманы түзгөн адам
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tasks',  # Колдонуучу түзгөн тапшырмалар
        verbose_name='Автору'
    )

    # ⭐ ДАЙЫНДАЛГАНДАР (Many to Many Field - Көп Колдонуучу)
    # Агайыңыз айткандай: Бир тапшырмага бир нече программист дайындалат.
    assigned_to = models.ManyToManyField(
        User,
        blank=True,
        related_name='assigned_tasks',  # Колдонуучу дайындалган тапшырмалар
        verbose_name='Дайындалган Программисттер'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Түзүлгөн күнү')

    # Мета-класс (Кошумча маалымат)
    class Meta:
        verbose_name = 'Тапшырма'
        verbose_name_plural = 'Тапшырмалар'
        ordering = ['-created_at']  # Жаңы тапшырмалар жогоруда турат

    def __str__(self):
        return self.title


# ⭐ ЖАҢЫ КОШУЛДУ: КОМАНДА (TEAM) МОДЕЛИ
class Team(models.Model):
    """Колдонуучулар топтошкон команда модели."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Команданын аты")
    description = models.TextField(blank=True, verbose_name="Сүрөттөмөсү")

    # Команда мүчөлөрү (ManyToManyField, User моделине шилтеме кылат)
    members = models.ManyToManyField(
        User,
        related_name='teams',  # Колдонуучуга кайрылуу: user.teams.all()
        verbose_name="Мүчөлөрү"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Түзүлгөн күнү')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Командалар"
        ordering = ['name']  # Аты боюнча иреттейбиз