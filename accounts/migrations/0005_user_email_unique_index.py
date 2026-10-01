from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_otpchallenge'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            WITH duplicates AS (
                SELECT id,
                       ROW_NUMBER() OVER (
                           PARTITION BY LOWER(COALESCE(email, ''))
                           ORDER BY id
                       ) AS row_num
                FROM auth_user
                WHERE email IS NOT NULL
            )
            DELETE FROM auth_user
            WHERE id IN (SELECT id FROM duplicates WHERE row_num > 1);

            CREATE UNIQUE INDEX IF NOT EXISTS auth_user_email_unique
            ON auth_user(email COLLATE NOCASE);
            """,
            reverse_sql="DROP INDEX IF EXISTS auth_user_email_unique;",
        ),
    ]
