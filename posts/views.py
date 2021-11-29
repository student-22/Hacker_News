from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer


class PostListCreateView(generics.ListCreateAPIView):
    """
        This API endpoint allows to get list of post and create post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentCreateView(generics.CreateAPIView):
    """
        This API endpoint allows to get list of comment and create comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


@api_view(['POST'])
@csrf_exempt
def upvote(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
        return Response(
            data={'message': f'{request.user.username} devoted on {post.title}'},
            status=status.HTTP_202_ACCEPTED
        )
    else:
        post.upvotes.add(request.user)
        return Response(
            data={'message': f'{request.user.username} voted on {post.title}'},
            status=status.HTTP_201_CREATED
        )