from django.conf import settings
from django.db import migrations


def assign_post_owner(apps, schema_editor):
    user_model = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    user = user_model.objects.order_by("id").first()
    if not user:
        return

    Post = apps.get_model("blog", "Post")
    Post.objects.filter(owner__isnull=True).update(owner=user)


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_post_owner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(assign_post_owner, migrations.RunPython.noop),
    ]
