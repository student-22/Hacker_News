# Generated by Django 3.2.9 on 2021-11-26 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_rename_context_comment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='score',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
