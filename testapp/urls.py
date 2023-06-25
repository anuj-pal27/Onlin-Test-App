from django.urls import path
from testapp.views import * 

urlpatterns = [
    path('',loginView,name='index'),
    # path('submitform/',submitform,name='submitform'),
    path('new-candidate',candidateRegistrationForm,name='CandidateRegistration'),
    path('store-candidate',candidateRegistration,name='storeCandidate'),
    # path('login',loginView,name='login'),
    path('home',candidateHome,name='home'),
    path('test-paper',testPaper,name='testPaper'),
    path('calculate-result',calculateTestResult,name='calculateTest'),
    path('test-history',testResultHistory,name='testHistory'),
    path('result',showTestResult,name='result'),
    path('logout',logoutView,name='logout'), 
]
