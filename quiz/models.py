from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length = 255)
    role = models.CharField(max_length = 10)

class Questions(models.Model):
    CHOICES = (
        ('op1', 'option1'),
        ('op2', 'option2'),
        ('op3', 'option3'),
        ('op4', 'option4'),
    )
    question = models.CharField(max_length=500, unique=True);
    option1 = models.CharField(max_length = 250);
    option2 = models.CharField(max_length = 250);
    option3 = models.CharField(max_length = 250);
    option4 = models.CharField(max_length = 250);
    answer = models.CharField(max_length  = 250, choices=CHOICES);
    topic = models.CharField(max_length = 20);

class Quiz(models.Model):
    STATUS = (
        ('1', 'Answered'),
        ('0', 'remaining'),
        ('-1', 'not Answered'),
    )
    que_id = models.ForeignKey(Questions, on_delete=models.CASCADE)
    ans = models.CharField(max_length = 250)
    status = models.CharField(max_length = 10, choices=STATUS, default='0')