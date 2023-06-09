# Generated by Django 4.1.7 on 2023-05-12 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('option1', models.CharField(max_length=250)),
                ('option2', models.CharField(max_length=250)),
                ('option3', models.CharField(max_length=250)),
                ('option4', models.CharField(max_length=250)),
                ('answer', models.CharField(choices=[('op1', 'option1'), ('op2', 'option2'), ('op3', 'option3'), ('op4', 'option4')], max_length=250)),
                ('topic', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ans', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('1', 'Answered'), ('0', 'remaining'), ('-1', 'not Answered')], default='0', max_length=10)),
                ('que_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.login')),
            ],
        ),
    ]
