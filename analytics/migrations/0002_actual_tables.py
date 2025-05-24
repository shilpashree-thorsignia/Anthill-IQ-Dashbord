from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('session_id', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, max_length=100, null=True)),
                ('user_message', models.TextField(blank=True, null=True)),
                ('bot_response', models.TextField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'conversations',
                'managed': False,
            },
        ),
    ] 