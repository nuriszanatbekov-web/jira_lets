# tasks/serializers.py
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # 'author' талаасы FK болгондуктан, анын username'ин гана көрсөтүү үчүн
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Task
        # API аркылуу жеткиликтүү боло турган талаалар
        fields = ('id', 'title', 'description', 'full_description', 'status', 'created_at', 'author', 'author_username')
        # 'author' талаасын окуу гана кылып коёбуз, анткени аны views-та автоматтык түрдө колдонуучу катары орнотобуз.
        read_only_fields = ('author',)