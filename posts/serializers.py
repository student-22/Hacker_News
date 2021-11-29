from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Post, Comment


class UpvoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'post', 'created',)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    upvotes_count = serializers.ReadOnlyField()
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'link', 'created', 'author', 'upvotes_count', 'comments_count')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        post = Post.objects.get(id=instance.id)
        response['comments_count'] = post.comments.count()
        return response


class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)
    upvotes = UpvoteSerializer(read_only=True, many=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'link', 'created', 'author', 'upvotes', 'comments')