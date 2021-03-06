# Generated by Django 3.1.5 on 2021-02-21 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_completedlesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='lessons.test')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='lessons.testquestion')),
            ],
        ),
    ]
