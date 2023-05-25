import os
import plotly.graph_objects as go
from plotly.offline import plot
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import *
from django.contrib import messages
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail

def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    context = {'blogs': Blogmodel.objects.filter(is_verified=True)}
    return render(request, 'home.html', context)


def base(request):
    return render(request, 'base.html')


def user_home(request):
    context = {'blogs': Blogmodel.objects.filter(is_verified=True)}
    return render(request, 'user_home.html', context)


def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('password')
        remember_me = request.POST.get('remember_me') 

        us = Registration.objects.filter(username=u, password=p)

        if len(us) == 1:
            request.session['username'] = us[0].username
            request.session['userid'] = us[0].id
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)

            # Show success message using Django's messaging framework
                messages.success(request, 'You have successfully logged in!')

            return redirect(user_home)
        else:
            msg = '<h1>Invalid UserName or Password!!!</h1>'
            context = {'msg1': msg}
            return render(request, 'login.html', context)
    else:
        msg = ''
        context = {'msg1': msg}
        return render(request, 'login.html')



def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = Blogmodel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)
    return render(request, 'blog_details.html', context)


def admin_home(request):
    return render(request, 'admin_home.html')


# def register_view(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         username = request.POST["username"]
#         password = request.POST["password"]
#         if Registration.objects.filter(username=username):
#             context = {'msg': "username already exist"}
#             return render(request, "register.html")
#         else:
#             reg = Registration(name=name, username=username, password=password)
#             reg.save()
#             return redirect('/login')
#     else:
#         return render(request, "register.html")

def register_view(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        password = request.POST["password"]
        c_password = request.POST["c_password"]
        
        if Registration.objects.filter(username=username):
            context = {'msg': "Username already exists."}
            return render(request, "register.html", context)
        elif password != c_password:
            context = {'msg': "Password and Confirm Password do not match."}
            return render(request, "register.html", context)
        else:
            reg = Registration(name=name, username=username, password=password)
            reg.save()
            return redirect('/login')
    else:
        return render(request, "register.html")



def add_blog(request):
    uid = request.session['userid']
    user = Registration.objects.get(id=uid)
    s = Blogmodel.objects.filter(user=user)

    context = {'form': BlogForm, 'user': user, 's': len(s)}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES.get('image')
            title = request.POST.get('title')
            uid = request.session['userid']
            user = Registration.objects.get(id=uid)
            author = user.name

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            if "blog" in request.POST:

                blog_obj = Blogmodel.objects.create(
                    user=user, title=title, author=author,
                    content=content, image=image
                )
                print(blog_obj)
                messages.success(request, 'Blog added successfully.')
                return render('/add_blog/')
            if "draft" in request.POST:

                print("in draft")
                new_draft = drafts(title=title, author=author,
                                   content=content, user=user, image=image)
                new_draft.save()
                messages.success(request, 'draft added successfully.')
                return render('/add_blog/')
    except Exception as e:
        print(e)
    return render(request, 'add_blog.html', context)


def see_blog(request):
    # context = {}

    # try:
    #     blog_objs = Blogmodel.objects.filter(user=request.user)
    #     B = Blogmodel.objects.get(user=request.user)
    #     # f = Feedbacks.objects.filter(title=B)
    #     context={'blog_objs': blog_objs}
    # except Exception as e:
    #     print(e)

    # print(context)
    uid = request.session['userid']
    user = Registration.objects.get(id=uid)
    blog_objs = Blogmodel.objects.filter(user=user)
    feedbacks = Feedbacks.objects.filter(blog__in=blog_objs)

    B = Blogmodel.objects.get(title='food')
    f = Feedbacks.objects.filter(blog=B)
    context = {'blog_objs': blog_objs, 'f': feedbacks}
    return render(request, 'see_blog.html', context)


def blog_update(request, slug):
    context = {}

    blog_obj = Blogmodel.objects.get(slug=slug)
    if blog_obj.is_verified == True:
        messages.success(request, 'Already published.')
        return redirect("/see_blog")

    # Check if the logged-in user is the author of the blog post

    # Populate the form with the current content of the blog post
    initial_dict = {'content': blog_obj.content}
    form = BlogForm(initial=initial_dict)
    if request.method == 'POST':
        form = BlogForm(request.POST)
        print(request.FILES)

        title = request.POST.get('title')
        user = request.user

        if form.is_valid():
            content = form.cleaned_data['content']
            print(content)
            blog_obj.title = title
            blog_obj.content = content
            if "image" in request:
                image = request.FILES["image"]
                blog_obj.image = image
            blog_obj.save()
            messages.success(request, 'Blog updated successfully.')
            return redirect("http://127.0.0.1:8000/see_blog")

    else:
        context['blog_obj'] = blog_obj
        context['form'] = form

        return render(request, 'blog_update.html', context)

def rate(request):
    if request.method == "POST":
        rate=request.POST["rating"]
        b=request.POST["id"]
        blog=Blogmodel.objects.get(id=b)
        s=blog.slug
        uid = request.session['userid']
        user = Registration.objects.get(id=uid)
        user_rate = Rating.objects.filter(title=blog,username=user).first()
        if user_rate == None:
            new_rate=Rating.objects.create(title=blog,username=user,rate=rate)
            new_rate.save()
            print("rated")
            average_rating = round(Rating.objects.filter(title=blog).aggregate(avg_rating=Avg('rate'))['avg_rating'])
            blog.ratings = average_rating
            blog.save()

            messages.success(request, "Thank you for rating the blog!")
            return redirect('blog_detail', slug=blog.slug)
        else:
            messages.warning(request, "You have already rated this blog.")
            return redirect('blog_detail', slug=blog.slug)

        

    

    

# def blog_delete(request, id):
#     try:
#         blog_obj = Blogmodel.objects.get(id=id)

#         if blog_obj.user == request.user:
#             blog_obj.delete()

#     except Exception as e:
#         print(e)

#     return redirect('/see_blog')


def blog_delete(request, id):
    blog_obj = Blogmodel.objects.get(id=id)
    blog_obj.delete()
    return redirect('/see_blog')


def admin_main(request):
    return render(request, 'admin_main.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def draft1(request):
    uid = request.session['userid']
    user = Registration.objects.get(id=uid)
    draf = drafts.objects.filter(user=user)
    context = {'draf': draf}
    return render(request, 'draft.html', context)


def blog_edit(request):
    return render(request, 'profile.html')


def draft_update(request, slug):
    context = {}

    try:
        blog_obj = drafts.objects.get(slug=slug)

        # Check if the logged-in user is the author of the blog post

        # Populate the form with the current content of the blog post
        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        title = blog_obj.title
        content = blog_obj.content
        author = blog_obj.author

        if request.method == 'POST':

            form = BlogForm(request.POST)
            print(request.FILES)
            if "image" in request.FILES:
                image = request.FILES["image"]
            else:
                image=blog_obj.image


            if "title" in request.POST:
                title = request.POST.get('title')

            uid = request.session['userid']
            user = Registration.objects.get(id=uid)
            
            if form.is_valid():
                if 'content' in request.POST:
                    content = form.cleaned_data['content']
                print(content)
                new_blog = Blogmodel.objects.create(
                    user=user, title=title, author=author,
                    content=content, image=image
                )
                new_blog.save()
                blog_obj.delete()
                return redirect("/draft")
        context['blog_obj'] = blog_obj
        context['form'] = form

    except Exception as e:
        print(e)

    return render(request, 'draft_update.html', context)


def draft_delete(request, id):
    draf = drafts.objects.get(id=id)
    draf.delete()
    return redirect('/draft')


def edit_profile(request):
    uname1 = request.session['username']
    u = Registration.objects.filter(username=uname1)
    x = Registration.objects.get(username=uname1)
    xemail = x.username
    context = {'user': u}
    if request.method == 'POST':
        up = Registration.objects.get(username=uname1)
        xemail = up.username
        name = request.POST.get('name')
        username = request.POST.get('username')
        if 'profile_pic' in request.FILES:
            u_file = request.FILES['profile_pic']
            fs = FileSystemStorage()
            userphoto = fs.save(u_file.name, u_file)
            up.profile_pic = userphoto

        # up.profile_pic=userphoto
        up.name = name
        up.username = username
        up.save()
        if xemail != up.username:
            return redirect(login_view)
        c = {'user': u, 'up': up}
        return render(request, 'profile.html', c)
    context = {'user': u}
    return render(request, 'edit_profile.html', context)


def profile(request):
    uname = request.session['username']
    u = Registration.objects.filter(username=uname)
    uid = request.session['userid']
    user = Registration.objects.get(id=uid)
    # num = Blogmodel.objects.filter(user=user).count()
    # num= Blogmodel.objects.all().count()
    num = Blogmodel.objects.filter(is_verified=True, user=user).count()
    context = {'user': u, 'num': num}
    return render(request, 'profile.html', context)


def search(request):
    title = request.GET.get('title')
    a = Blogmodel.objects.filter(title__icontains=title, is_verified=True)
    message = ''

    if not a:
        message = f'Hmmm, we could not find any matches for "{title}". Try again!!'

    return render(request, 'search.html', {'a': a, 'message': message})






