# Generated by Django 4.1 on 2022-09-05 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_is_editor'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempPassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(blank=True, max_length=64)),
            ],
        ),
    ]
