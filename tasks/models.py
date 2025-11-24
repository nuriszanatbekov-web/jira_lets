from django.db import models
from django.contrib.auth.models import User  # 1. User моделин импорттоо


class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'Todo'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done')
    ]

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    full_description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    created_at = models.DateTimeField(auto_now_add=True)

    # 2. АВТОР ТАЛААСЫН КОШУУ
    # models.ForeignKey(User, ...) User моделине шилтеме берет.
    # on_delete=models.SET_NULL: Эгер автор өчүрүлсө, тапшырманын автору "null" болуп калат.
    # null=True, blank=True: Бул талаанын бош болушуна уруксат берет (эски тапшырмалар үчүн маанилүү).
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title