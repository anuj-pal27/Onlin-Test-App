from urllib import request
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

from testapp.models import Candidate, Question, Result
import random
# Create your views here.

# def index(request):
#     return render(request,'index.html')

def submitform(request):
   pass
    
def candidateRegistrationForm(request):
    return render(request,'registration_form.html')

def candidateRegistration(request):
    if request.method=='POST':
        username=request.POST['username']
        #Check if the user already exists
        
        if(len(Candidate.objects.filter(username=username))):
            userStatus=1
        else:
            candidate=Candidate()
            candidate.username=username
            candidate.password=request.POST['password']
            candidate.name=request.POST['name']
            candidate.save()
            userStatus=2
    else:
        userStatus=3 #Request method is not Post
    context={'userStatus':userStatus}
    return render(request,'registration_form.html',context)
def loginView(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        candidate=Candidate.objects.filter(username=username,password=password)
        if len(candidate)==0:
            loginError="Invalid username or password"
            res=render(request,'index.html',{'loginError':loginError})
        else:
            #login Success
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res=HttpResponseRedirect('home')
    else:
        res=render(request,'index.html')
    return res

def candidateHome(request):
    if 'name' not in request.session.keys():
        return render(request,"index.html")

    else:
        res=render(request,'home.html')
        return res
def testPaper(request):
    if 'name' not in request.session.keys():
        return render(request,"index.html")
    #fetch questions from database table
    n=int(request.GET['n'])
    question_pool=list(Question.objects.all())
    random.shuffle(question_pool)
    question_list=question_pool[:n]
    context={'questions':question_list}
    return render(request,'test_paper.html',context)

def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question=Question.objects.get(qid=n)
        try:
            if question.ans==request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
    points=(total_right-total_wrong)/len(qid_list)*10
    #store result in Result Table
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username'])
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.points=points
    result.save()

    #update candidate Table

    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted+=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted
    candidate.save()
    res=HttpResponseRedirect('result')
    return res
def testResultHistory(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    
    candidate=Candidate.objects.filter(username=request.session['username'])
    results=Result.objects.filter(username_id=candidate[0].username)
    context={'candidate':candidate[0],'results':results}
    return render(request,'candidate_history.html',context)

def showTestResult(request):
    if 'name' not in request.session.keys():
        res=HttpResponseRedirect("login")
    result=Result.objects.filter(resultid=Result.objects.latest('resultid').resultid,username_id=request.session['username'])
    context={'result':result}
    res=render(request,'show_result.html',context)
    return res

def logoutView(request):
    if 'name' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return render(request,"index.html")
