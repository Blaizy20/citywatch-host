from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_announcement_categories_image_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='category',
            field=models.CharField(
                choices=[
                    ('road', 'Road'),
                    ('streetlight', 'Streetlight'),
                    ('drainage', 'Drainage/Flooding'),
                    ('facility', 'Public Facility'),
                    ('pets', 'Pets and Animals'),
                    ('other', 'Others'),
                ],
                max_length=20,
            ),
        ),
    ]