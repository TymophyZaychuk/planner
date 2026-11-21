from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def copy_comment_authors(apps, schema_editor):
    Comment = apps.get_model('tasks_app', 'Comment')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
    alias = schema_editor.connection.alias

    for comment in Comment.objects.using(alias).all().iterator():
        username = comment.commented_by
        user = User.objects.using(alias).filter(username=username).first()
        if user:
            Comment.objects.using(alias).filter(pk=comment.pk).update(
                commented_by_user_id=user.pk
            )


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_app', '0003_alter_task_priority_alter_task_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commented_by_user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(copy_comment_authors, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='comment',
            name='commented_by',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='commented_by_user',
            new_name='commented_by',
        ),
    ]
