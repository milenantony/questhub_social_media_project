from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import date


# Create your views here.


# register page

def registerpage(request):
    return render(request,'register.html') 


def register_save(request):
    if request.POST:
        username=request.POST['uname']
        password=request.POST['pswd'] 
        email=request.POST['email']   
        
        if Registerprofile.objects.filter(username=username).exists():
            messages.info(request,'Username already exists')
            return redirect('registerpage') 
        elif Registerprofile.objects.filter(email=email).exists():
            messages.info(request,'Email id already exists')
            return redirect('registerpage')
        else :
            register=Registerprofile(username=username,password=password,email=email,)
            register.save()
            messages.success(request,'Your account registered successfully')
            return redirect('loginpage')

    else:
        return redirect('registerpage')    


# login page

def loginpage(request):
    return render(request,'login.html')    

def userlogin(request):
    if request.POST:
        username = request.POST.get('uname', '')  
        password = request.POST.get('pswd', '')  

        try:
            log_details = Registerprofile.objects.get(username=username, password=password)

        except ObjectDoesNotExist:

            messages.error(request, 'No account found')
            return redirect('loginpage')

        if log_details.position == 'User':
            request.session["user_id"] = log_details.id
            if 'user_id' in request.session:
                if request.session.has_key('user_id'):
                    user_id = request.session['user_id']
                else:
                    return redirect('/')

                user_dash = Registerprofile.objects.get(id=user_id)

                if user_dash:
                    messages.success(request, 'Login Successful')
                    
                    return redirect('index')
                else:
                    return redirect('loginpage')

    return redirect('loginpage')

def userlogout(request):
    request.session.pop('user_id', None)
    messages.success(request,'Logout successfully')
    return redirect('loginpage')


# home page

def index(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        questions=Questions.objects.all().order_by('-date','-time')

        context={
            'userdata':userdata,
            'questions':questions,
            'user_id':user_id,
        }

    return render(request, 'index.html', context)

def filter_today(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        userdata = Registerprofile.objects.get(id=user_id)
        
        today = str(date.today())
        questions = Questions.objects.filter(date=today).order_by('-date', '-time')

        context = {
            'userdata': userdata,
            'questions': questions,
            'user_id': user_id,
        }
        return render(request, 'index.html', context)
    else:
        return redirect('/')

def filter_myposts(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        userdata = Registerprofile.objects.get(id=user_id)
        
        questions = Questions.objects.filter(user=userdata).order_by('-date', '-time')

        context = {
            'userdata': userdata,
            'questions': questions,
            'user_id': user_id,
        }
        return render(request, 'index.html', context)
    else:
        return redirect('/')




# ask a question section

def askquestion(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')

        user=Registerprofile.objects.get(id=user_id)
        if request.POST:
            question=request.POST['question']
            data=Questions(user=user,question=question)
            data.save()
            messages.success(request,'Question posted')
            return redirect('index')

    else:
        return redirect('/')


# submit answer to a question

def submit_answer(request,pk):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')

        user=Registerprofile.objects.get(id=user_id)
        question=Questions.objects.get(id=pk)

        # Check if the user has already answered this question
        existing_answer = Answer.objects.filter(user=user, question=question)
        if existing_answer.exists():
            messages.info(request,'Already answered..!')
            return redirect('index')

        if request.POST:
            answer_text=request.POST['answer_text']
            data=Answer(answer_text=answer_text,user=user,question=question)
            data.save()
            messages.success(request,'Answered')
            return redirect('index')
        
    else:
        return redirect('/')


# View answers of a question

def view_answers(request,pk):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        question=Questions.objects.get(id=pk)
        answers=Answer.objects.filter(question=question).order_by('-date','-time')
        print(answers)

        context={
            'userdata':userdata,
            'question':question,
            'answers':answers,
            'user_id':user_id,
        }
    return render(request,'answers.html',context)


# like answers

def like_answer(request, answer_id):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id).id
        if request.method == 'GET' :
            try:
                answer = get_object_or_404(Answer, id=answer_id)

                # Check if the user has already liked this answer to prevent double-liking
                if userdata in answer.likes.all():
                    return JsonResponse({'success': False, 'error': 'You have already liked this answer.'})

                # Add the user to the likes
                answer.likes.add(userdata)

                like_count = answer.like_count()

                return JsonResponse({'success': True, 'like_count': like_count})
            except Answer.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Answer not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def profilepage(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        questions = Questions.objects.filter(user=userdata).order_by('-date', '-time')

        
        context={
            'userdata':userdata,
            'user_id':user_id,
            'questions':questions,
        }
        return render(request,'profile.html',context)
    else:
        return redirect('/')

def edit_profile(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        
        context={
            'userdata':userdata,
            'user_id':user_id,
        }
        return render(request,'edit_profile.html',context)
    else:
        return redirect('/')

def edit_profile_save(request):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)

        if request.POST:
            new_pic=request.FILES.get('profile_pic')
            phone=request.POST['phone']
            gender=request.POST['gender']
            userdata.name=request.POST['name']
            userdata.username=request.POST['username']
            userdata.email=request.POST['email']
            userdata.bio=request.POST['bio']
            userdata.gender=request.POST['gender']
            userdata.phone_number=phone
            userdata.place=request.POST['place']
            if new_pic:
                userdata.profile_picture=new_pic
            print(new_pic)
            userdata.save()
            messages.success(request,'Profile Updated')
            return redirect("profilepage")   
            
    else:
        return redirect('/')


def delete_post(request,pk):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        userdata = Registerprofile.objects.get(id=user_id)
        question=Questions.objects.get(id=pk,user=userdata)
        question.delete()
        messages.success(request,'Post Deleted Successfully')
        return redirect('profilepage')    
    else:
        return redirect('/')

def edit_post(request,pk):
    if 'user_id' in request.session:
        if request.session.has_key('user_id'):
            user_id = request.session['user_id']
           
        else:
            return redirect('/')
        
        question=Questions.objects.get(id=pk)

        if request.POST:
            question.question=request.POST['question']
            question.save()
            messages.success(request,'Post edited successfully')
            return redirect("profilepage")   
            
    else:
        return redirect('/')

