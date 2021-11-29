from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver


from .models import Post, Comment


@receiver(m2m_changed, sender=Post.upvotes.through)
def post_upvotes_changed(sender, instance, **kwargs):
    instance.upvotes_count = instance.upvotes.count()
    instance.save()


# @receiver(pre_save, sender=Comment)
# def post_comments_changed(sender, instance, **kwargs):
#     post = Post.objects.get(pk=instance.post.pk)
#     post.comments_count = post.comments.count() + 1
#     post.save()