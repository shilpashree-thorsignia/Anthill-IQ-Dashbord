from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('analytics', '0007_handle_duplicate_session_ids'),
    ]

    operations = [
        # First, ensure the users table has a proper primary key
        migrations.RunSQL(
            """
            -- Add id column if it doesn't exist
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                             WHERE table_name = 'users' AND column_name = 'id') THEN
                    ALTER TABLE users ADD COLUMN id SERIAL PRIMARY KEY;
                END IF;
            END $$;
            """,
            reverse_sql=""
        ),
        
        # Create a temporary column for the new user_id
        migrations.RunSQL(
            """
            ALTER TABLE conversations 
            ADD COLUMN new_user_id INTEGER;
            """,
            reverse_sql=""
        ),
        
        # Update the temporary column with the correct user IDs
        migrations.RunSQL(
            """
            UPDATE conversations c
            SET new_user_id = u.id
            FROM users u
            WHERE c.user_id = u.session_id;
            """,
            reverse_sql=""
        ),
        
        # Drop the old foreign key constraint if it exists
        migrations.RunSQL(
            """
            ALTER TABLE conversations 
            DROP CONSTRAINT IF EXISTS conversations_user_id_fkey;
            """,
            reverse_sql=""
        ),
        
        # Drop the old user_id column and rename new_user_id
        migrations.RunSQL(
            """
            ALTER TABLE conversations 
            DROP COLUMN user_id;
            
            ALTER TABLE conversations 
            RENAME COLUMN new_user_id TO user_id;
            """,
            reverse_sql=""
        ),
        
        # Add the new foreign key constraint
        migrations.RunSQL(
            """
            ALTER TABLE conversations 
            ADD CONSTRAINT conversations_user_id_fkey 
            FOREIGN KEY (user_id) 
            REFERENCES users(id) 
            ON DELETE CASCADE;
            """,
            reverse_sql=""
        ),
        
        # Update the model fields
        migrations.AlterField(
            model_name='conversation',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='conversations',
                to='analytics.user',
                db_column='user_id'
            ),
        ),
    ] 