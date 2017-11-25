from rest_framework import serializers
from LinkGrabberDjango.models import Post


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'rating', 'poster', 'year')