from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import User

# Create your views here.
 

def indexPage(request, posts="all" , grid=4):
   
   posts = Post.objects.all().order_by("?")[:1]
   context = {
      "categorys" : Category.objects.all(),
      "posts":posts,
      "grid": grid,
   }
   return render(request, 'index.html', context)


def card_listPage(request, cate="all", grid=4):

   if cate != "all":
      posts = Post.objects.filter(category__title=cate)
   else:
      posts = Post.objects.all()
   categorys = Category.objects.all()
   context = {
      "posts":posts,
      "cate": cate,
      "grid": grid,
      "categorys": categorys,
   }
   return render(request, 'card_list.html', context)

def detailPage(request, pid): # fnksiyonlar ve sayfalar GET ile çalışırlar
   comments = Comment.objects.filter(post=pid)
   post = Post.objects.get(id=pid)

   if request.method == "POST":
      fullname = request.POST.get("fullname")
      text = request.POST.get("comment")

      comment = Comment(full_name=fullname, text=text, post=post)
      comment.save()
      
   
   context = {
      "comments": comments,
      "post": post,
      "categorys": Category.objects.all(),
   }
   return render(request, 'detail.html', context)



# ==== User ==== 
def loginPage(request):
   username = ""
   password = ""
   hata = None
   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      
   user = authenticate(username=username, password=password )
   
   if user is not None:
      login(request, user)
      return redirect('/')
   else:
      hata = "Kullanıcı adı veya şifre yanlış!"
      
   context={
      "hata":hata,
   }
   return render(request, 'user/login.html', context)

def registerPage(request):
   hata = None
   user = None
   # fname = ""
   # lname = ""
   # email = ""
   # password = ""
   # password2 = ""
   
   if request.method == "POST":
      username = request.POST.get("username")
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      email = request.POST.get("email")
      password = request.POST.get("password")
      password2 = request.POST.get("password2")
      checkbox = request.POST.get("checkbox")
      
      if checkbox is None:  
         hata = "Formu onaylayınız!"
      else:
         if password == password2:
            if not User.objects.filter(username=username).exists():
               if not User.objects.filter(email=email).exists():
                  user = User.objects.create_user(username=username,first_name=fname,last_name=lname, email=email,password=password2, )
                  user.save()
                  return redirect('/Giris/')
               else:
                  hata ="Bu email zaten kullanılıyor! "
            else:
               hata ="Bu  kullanıcı adı zaten mevcut başka bir tane deneyin!"      
              
   if user is not None:
      registerPage(request, user, fname, lname) 
      
   context = {
      "hata":hata
   }
   return render(request, 'user/register.html', context)

def logoutUser(request):
   logout(request)
   return redirect("loginPage")