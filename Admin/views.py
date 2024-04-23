from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from questhub_app.models import Registerprofile,Questions, Answer
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages




# Create your views here.
@login_required(login_url='loginpage')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

@login_required(login_url='loginpage')
def user_list(request):
    # Fetch all instances of Registerprofile model
    users = Registerprofile.objects.all()
    return render(request, 'user_list.html', {'users': users})


@login_required(login_url='loginpage')
def user_details(request, user_id):
    # Fetch user details based on user_id
    user = Registerprofile.objects.get(pk=user_id)
    questions=Questions.objects.filter(user=user_id).order_by('-date','-time')
    answers=Answer.objects.filter(question__in=questions).order_by('-date','-time')
    # Render the user_details.html template with user data
    print(questions)
    print(answers)
    context={
        'user': user,
        'questions':questions,
        'answers':answers
    }
    
    return render(request, 'user_details.html', context)

@login_required(login_url='loginpage')
def delete_user(request, user_id):
    user = get_object_or_404(Registerprofile, id=user_id)
    user.delete()
    messages.success(request, 'User has been deleted Successfully.')
    return redirect('user_list')

@login_required(login_url='loginpage')
def delete_question(request,pk):
    question=Questions.objects.get(id=pk)
    user=Registerprofile.objects.get(id=question.user.id)
    
    question.delete()
    messages.success(request,'Post Deleted Successfully')
    return redirect('user_details',user.id)    
    


