# Generated by Django 3.2.5 on 2021-08-02 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_alter_article_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
    ]
