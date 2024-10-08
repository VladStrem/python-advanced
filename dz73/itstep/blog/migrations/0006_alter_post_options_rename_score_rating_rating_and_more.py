# Generated by Django 5.0.7 on 2024-08-16 19:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['publish'], 'verbose_name': 'Публікації', 'verbose_name_plural': 'Публікації'},
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='score',
            new_name='rating',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='blog.category'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('post', 'user')},
        ),
    ]
