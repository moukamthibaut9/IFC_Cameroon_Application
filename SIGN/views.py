from django.shortcuts import render, redirect
from SIGN.forms import ConnexionForm, RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

sel='#(*)&(^)#'

def sign_up(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('password1')==form.cleaned_data.get('password2'):
                for user in User.objects.all():
                    if form.cleaned_data.get('username')==user.username:
                        messages.error(request,"Le nom d'utilisateur que vous avez entré est déjà pris")
                        bad_username=True
                        break
                if 'bad_username' in locals():
                    return render(request,'sign_up.html',
                        {
                            'registration_form':form,
                        }
                    )    
                user_password=form.cleaned_data.get('password1')[:-5]+sel+form.cleaned_data.get('password1')[-5:]
                user=User.objects.create_user(email=form.cleaned_data['email'],
                                            username=form.cleaned_data['username'],
                                            password=user_password)
                if user is not None:
                    return redirect('sign_in')
                else:
                    messages.error(request,"Une problème est survenue durant le traitement de votre requête. Veillez reéssayer.")
                    return render(request,'sign_up.html',
                        {
                            'registration_form':form,
                        }
                    )
            else:
                messages.error(request,"Vous avez entré deux mots de passe différents.")
                return render(request,'sign_up.html',
                    {
                        'registration_form':form,
                    }
                )    
            
        else:
            return render(request,'sign_up.html',
                {
                    'registration_form':form,
                }
            )
    form=RegistrationForm()
    return render(request,'sign_up.html',
                {
                    'registration_form':form,
                }
            )

def sign_in(request):
    if request.method=='POST':
        form=ConnexionForm(request.POST)
        if form.is_valid():
            user_password=form.cleaned_data.get('password')[:-5]+sel+form.cleaned_data.get('password')[-5:]
            user=authenticate(username=form.cleaned_data['username'],password=user_password)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request,"OUPS! La connexion a échouée. Vérifiez que vos informations sont correctes.")
                return render(request,'sign_in.html',
                    {
                        'connexion_form':form,
                    }
                )
        else:
            return render(request,'sign_in.html',
                    {
                        'connexion_form':form,
                    }
                )
    form=ConnexionForm()
    return render(request,'sign_in.html',
                {
                    'connexion_form':form,
                }
            )
def sign_out(request):
    for user in User.objects.filter(is_superuser=False):
        logout(request)
    return redirect('home')
