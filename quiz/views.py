from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from quiz.models import Login,Questions,Quiz
from django.db import IntegrityError
from django.http import HttpResponse
import random
from django.core import serializers

def login_view(request):
    if request.method == 'POST':
        # obj = Login.objects.get(username=request.POST.get('username'))
        try:
            obj = Login.objects.get(username=request.POST.get('username'))
        except Login.DoesNotExist:
            contex = {
                'msg':"Username is not exist"
            }
            return render(request,'login.html',contex)
        
        role = obj.role
        password = obj.password
        if password != request.POST.get('password') :
            contex = {
                'msg':"password is invalid"
            }
            return render(request,'login.html',contex)
        request.session['username'] = request.POST['username']
        contex = {
            'username' : request.POST['username']
        }
        if role == 'admin':
            return render(request, 'adminhome.html', contex)
        else:
            return render(request, 'userhome.html', contex)           
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        
        try:
            user = Login()
            user.username = request.POST.get('username')
            user.password = request.POST.get('password')
            user.role = request.POST.get('role')
            user.save()
        except IntegrityError:
            msg = 'User already exists!'
            contex = {
                'msg': msg
            }
            return render(request,'signup.html',contex)
        request.session['username'] = request.POST['username']
        contex = {
                'username' : request.POST['username'],
                'msg' : "singup is done!!"
        }
        
        if user is not None:
            if user.role == 'admin':  # note the change here: compare role.role to 'admin'
                return render(request, 'adminhome.html', contex)
            else:
                return render(request, 'userhome.html', contex)
    else:
        return render(request, 'signup.html')

def logout_view(request):
    request.session.flush()
    return redirect('/')

def Que(request):
    return render(request,'que.html')

def addQue(request):
    try:
        q = Questions.objects.create(question=request.POST.get('question'))
    except IntegrityError:
        msg = 'Question already exists!'
        contex = {
            'msg':msg
        }
        return render(request,'que.html',contex)
    q.question = request.POST.get('question')
    q.option1 = request.POST.get('option1')
    q.option2 = request.POST.get('option2')
    q.option3 = request.POST.get('option3') 
    q.option4 = request.POST.get('option4')
    q.answer = request.POST.get('answer')
    q.topic = request.POST.get('topic')
    q.save()
    return render(request,'adminhome.html')

def adminhome(request):
    contex = {
        'username' : request.session['username']
    }
    return render(request,'adminhome.html',contex)

def userhome(request,topic=None):
    contex = {
        'username' : request.session['username']
    }
    return render(request,'userhome.html',contex)

def quiz(request):
    topics = Questions.objects.values_list('topic', flat=True).distinct()
    context = {
        'topics': topics,
        'username' : request.session['username']
    }
    return render(request, 'topic.html', context)

def exam(request, topic):
    questions = Questions.objects.filter(topic=topic)
    random.shuffle(list(questions))
    if len(questions) > 10:
        questions = random.sample(list(questions), 10)
        request.session['questions'] = serializers.serialize('json', questions)
    elif len(questions) < 10:
        context = {
            'msg' : "Not enough questions"
        }
        return render(request,'topic.html',context)
    request.session['topic'] = topic
    context = {'question': questions[0], 'topic': topic}
    return render(request, 'q1.html', context)

def q1(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {'question': q[0], 'topic': topic}
    return render(request, 'q1.html', context)
def q2(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question1')
    quiz = Quiz()
    quiz.que_id = q[0]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()

    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'question' : q[1],
    }

    return render(request,'q2.html',context)

def q3(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question2')
    quiz = Quiz()
    quiz.que_id = q[1]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'question' : q[2],
    }

    return render(request,'q3.html',context)

def q4(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question3')
    quiz = Quiz()
    quiz.que_id = q[2]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'question' : q[3],
    }

    return render(request,'q4.html',context)

def q5(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question4')
    quiz = Quiz()
    quiz.que_id = q[3]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'question' : q[4],
    }

    return render(request,'q5.html',context)

def q6(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question5')
    quiz = Quiz()
    quiz.que_id = q[4]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'question' : q[5]
    }

    return render(request,'q6.html',context)

def q7(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question6')
    quiz = Quiz()
    quiz.que_id = q[5]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'q6' : Quiz.objects.filter(que_id=q[5]).last(),
        'question' : q[6],
    }

    return render(request,'q7.html',context)

def q8(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question7')
    quiz = Quiz()
    quiz.que_id = q[6]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'q6' : Quiz.objects.filter(que_id=q[5]).last(),
        'q7' : Quiz.objects.filter(que_id=q[6]).last(),
        'question' : q[7],
    }

    return render(request,'q8.html',context)

def q9(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question8')
    quiz = Quiz()
    quiz.que_id = q[7]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'q6' : Quiz.objects.filter(que_id=q[5]).last(),
        'q7' : Quiz.objects.filter(que_id=q[6]).last(),
        'q8' : Quiz.objects.filter(que_id=q[7]).last(),
        'question' : q[8],
    }

    return render(request,'q9.html',context)

def q10(request,topic=None) :
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question9')
    quiz = Quiz()
    quiz.que_id = q[8]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'q6' : Quiz.objects.filter(que_id=q[5]).last(),
        'q7' : Quiz.objects.filter(que_id=q[6]).last(),
        'q8' : Quiz.objects.filter(que_id=q[7]).last(),
        'q9' : Quiz.objects.filter(que_id=q[8]).last(),
        'question' : q[9]
    }

    return render(request,'q10.html',context)


def backq1(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {'question': q[0], 'topic': topic}
    return render(request,'q1.html',context)

def backq2(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'question' : q[1],
    }

    return render(request,'q2.html',context)

def backq3(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'question' : q[2],
    }

    return render(request,'q3.html',context)

def backq4(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'question' : q[3],
    }

    return render(request,'q4.html',context)

def backq5(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'question' : q[4],
    }

    return render(request,'q5.html',context)

def backq6(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'question' : q[5],
    }

    return render(request,'q6.html',context)

def backq7(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'q6' : Quiz.objects.filter(que_id=q[5]).last(),
        'question' : q[6],
    }

    return render(request,'q7.html',context)

def backq8(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'q6' : Quiz.objects.filter(que_id=q[5]).last(),
        'q7' : Quiz.objects.filter(que_id=q[6]).last(),
        'question' : q[7],
    }

    return render(request,'q8.html',context)

def backq9(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    context = {
        'q1' : Quiz.objects.filter(que_id=q[0]).last(),
        'q2' : Quiz.objects.filter(que_id=q[1]).last(),
        'q3' : Quiz.objects.filter(que_id=q[2]).last(),
        'q4' : Quiz.objects.filter(que_id=q[3]).last(),
        'q5' : Quiz.objects.filter(que_id=q[4]).last(),
        'q6' : Quiz.objects.filter(que_id=q[5]).last(),
        'q7' : Quiz.objects.filter(que_id=q[6]).last(),
        'q8' : Quiz.objects.filter(que_id=q[7]).last(),
        'question' : q[8],
    }

    return render(request,'q9.html',context)

def result(request,topic=None):
    questions = request.session.get('questions')
    questions = serializers.deserialize('json', questions)
    q = [q.object for q in questions]
    ans = request.POST.get('question10')
    quiz = Quiz()
    quiz.que_id = q[9]
    if ans is not None:
        quiz.status = '1'
        quiz.ans = ans
    else:
        quiz.status = '-1'
    quiz.save()
    marks = 0
    for question in q:
        print(question)
        quiz = Quiz.objects.filter(que_id=question).last()
        if(quiz.status == '1'):
            correct = question.answer
            a = quiz.ans
            if correct == 'option1' and a == 'op1':
                print('++')
                marks += 1
            elif correct == 'option2' and a == 'op2':
                print('++')
                marks += 1
            elif correct == 'option3' and a == 'op3':
                print('++')
                marks += 1
            elif correct == 'option4' and a == 'op4':
                print('++')
                marks += 1
            else:
                marks -= 0.33
                print('--')
    context = {
        'topic' : request.session.get('topic'),
        'marks' : marks,
        'username' : request.session.get('username'),
    }

    return render(request,'result.html',context)