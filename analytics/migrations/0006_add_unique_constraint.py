from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('analytics', '0005_remove_useractivity_user_delete_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='session_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ] 