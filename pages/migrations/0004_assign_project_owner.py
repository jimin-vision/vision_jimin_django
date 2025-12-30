from django.conf import settings
from django.db import migrations


def assign_project_owner(apps, schema_editor):
    user_model = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    user = user_model.objects.order_by("id").first()
    if not user:
        return

    Project = apps.get_model("pages", "Project")
    Project.objects.filter(owner__isnull=True).update(owner=user)


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_project_owner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(assign_project_owner, migrations.RunPython.noop),
    ]
