from django.db import migrations

def handle_duplicate_session_ids(apps, schema_editor):
    User = apps.get_model('analytics', 'User')
    db_alias = schema_editor.connection.alias
    
    # Get all users ordered by timestamp
    users = User.objects.using(db_alias).order_by('timestamp')
    
    # Keep track of seen session_ids
    seen_session_ids = set()
    
    # For each user
    for user in users:
        if user.session_id in seen_session_ids:
            # If we've seen this session_id before, make it unique by appending timestamp
            user.session_id = f"{user.session_id}_{user.timestamp.strftime('%Y%m%d%H%M%S')}"
            user.save()
        else:
            seen_session_ids.add(user.session_id)

class Migration(migrations.Migration):
    dependencies = [
        ('analytics', '0006_add_unique_constraint'),
    ]

    operations = [
        migrations.RunPython(handle_duplicate_session_ids),
    ] 