from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_announcement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='announcement_type',
            field=models.CharField(
                choices=[
                    ('news', 'News'),
                    ('advisory', 'Advisory'),
                    ('schedule', 'Schedule'),
                    ('announcement', 'Announcement'),
                    ('event', 'Event'),
                ],
                default='news',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='announcement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='announcement_images/'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='event_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]