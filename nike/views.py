from django.db.models import ExpressionWrapper,F
from django.db.models import Avg,Max,Min,Sum,Count,DecimalField
from django.db.models.functions import Round
from django.shortcuts import get_object_or_404, render,redirect
from django.http import Http404, HttpResponse
from nike.form import BlogForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from .models import Blog,Book
import os

try:
    from supabase import create_client
except ImportError:
    create_client = None


# Create your views here.

#supabase storage integration

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def upload_file(file):
    file_content = file.read()
    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(file.name, file_content)
    return supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file.name)


def home(request):
    return render(request, 'nike.html')
    #return HttpResponse("helloo")
def forgot_password(request):
    return render(request,'forgot_password.html')
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('signup')
        else:
            messages.info(request, "Invalid credentials.") 
            return render(request,'nike_register.html', {'form': form})  
    else:
        form = UserForm()
    return render(request,'nike_register.html', {'form': form})
def signup(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('nike1') 
             # Redirect to a success page
            else:
                messages.info(request, "User not Found.")
        else:
            print(form.errors)  # shows errors in console
            messages.error(request, form.errors)  # shows errors in template
    else:
        form = AuthenticationForm()
    return render(request, 'signup.html', {'form': form})
@login_required
def nike1(request):
    return render(request,'nike1.html')
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request,'Logged out successfully.')
    return redirect('signup')
#@login_required
# #def change_password(request):
#     #form = PasswordChangeForm(user = request.user)
#     #if request.method == 'POST':
#       #  form = PasswordChangeForm(user = request.user,data = request.POST)
#        # if form.is_valid():
#             #user = form.save()
#             #update_session_auth_hash(request,user)
#            # messages.success(request,"Password changed successfully.")
#             #return redirect('signup')
#         else:
#             messages.info(request, "Invalid credentials.")
#           #  return redirect('change_password') 
#     else:
#         form = PasswordChangeForm(user = request.user)
#         return render(request,"change_password.html",{'form':form})
@login_required
def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("signup")

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = PasswordChangeForm(user=request.user)

    return render(
        request,
        "change_password.html",
        {"form": form}
    )
@login_required
@permission_required('nike.add_blog', raise_exception = True)
def add_blog_post(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request,"Blog post added successfully.")
        else:
            messages.info(request, "Blog not Posted.")
            return render(request, 'add_blog_post.html', {'form': form})
    else:
        form = BlogForm()
    return render(request, 'add_blog_post.html', {'form': form})

@login_required
@permission_required('nike.change_blog', raise_exception = True)
def edit_blog_post(request, post_id):
    post = get_object_or_404(Blog, id=post_id)
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post.title   = form.cleaned_data.get("title")
            post.content = form.cleaned_data.get('content')
            post.picture = form.cleaned_data.get('picture')
            post.save()
            messages.success(request,"Blog post updated successfully.")
        else:
            messages.error(request,"Failed to update blog post.")
        return redirect('view_posts')
    
    return render(request, 'edit_blog_post.html',{"post": post})


@login_required
#@permission_required('nike.view_blog', raise_exception = True)
def view_posts(request):
    posts = Blog.objects.all()
    return render(request, 'view_posts.html', {'posts': posts})

                                                                 
@login_required
@permission_required('nike.delete_blog', raise_exception = True)
def delete_blog_post(request,post_id):
    post = get_object_or_404(Blog,id = post_id)
    if request.method == "POST":
        post.delete()
        messages.success(request,"Blog post deleted successfully.")
        return redirect('view_posts')
    return render(request, 'delete_blog_post.html', {'post': post})

#Basic DB Queries 

def basic_queries(request):
    try:
        all_books = Book.objects.all() # SELECT * FROM Book
        filtered_books = Book.objects.filter(language='English') # SELECT * FROM Book WHERE language='English'
        excluded_books = Book.objects.exclude(price__gt=300)  # SELECT * FROM Book WHERE NOT price >= 300
        oderded_books = Book.objects.order_by('published_date') # SELECT * FROM Book ORDER BY published_date 
        get_book = Book.objects.get(id=3)

        context = {
            'all_books': all_books,
            'filtered_books': filtered_books,
            'excluded_books': excluded_books,
            'odered_books': oderded_books,
            'get_book': get_book
        }

        return render(request, 'basic_queries.html', {"context": context})
    except Book.DoesNotExist:
        raise Http404("Book not found.")

#aggregate functions

def aggregate_functions(request):
    try:
        average_price = Book.objects.aggregate(Avg('price'))
        max_price = Book.objects.aggregate(Max('price'))
        min_price = Book.objects.aggregate(Min('price'))
        total_price = Book.objects.aggregate(Sum('price'))
        author_count = Book.objects.aggregate(Count('author'))
        annotated_books = Book.objects.annotate(
            discounted_price = ExpressionWrapper(
                Round(F('price')*0.9,2),
                output_field = DecimalField(max_digits=6, decimal_places=2)
            )
        )
        return render(request, 'aggregate_functions.html', {
            'average_price': average_price,
            'max_price': max_price,
            'min_price': min_price,
            'total_price': total_price,
            'author_count': author_count,
            'annotated_books': annotated_books
        })
    except Book.DoesNotExist:
        raise Http404("Book not found.")

#F_expressions

def f_expressions(request):
    try:
        Book.objects.update(price=F('price')+50)
        books = Book.objects.all()
        return render(request, 'f_expressions.html', {'books': books})
    except Book.DoesNotExist:
        raise Http404("Book not found.")

#raw_queiries
 
def raw_queries(request): 
    try:
        books = Book.objects.raw('SELECT * FROM nike_book WHERE price > %s',[350])
        return render(request,'raw_queries.html',{"books":books})
    except Book.DoesNotExist:
        raise Http404("Book Not Found!")

#solving (n+1) problems

def relational_queries(request):
    try:
        books = Book.objects.select_related('author').all()
        return render(request,'relational_queries.html',{'books':books})
    except Book.DoesNotExist:
        raise Http404("Book does not exist!")  

#custom_queries: each query as a function using models

def custom_queries(request):
    expensive_books = Book.objects.expensive()
    return render(request,'custom_queries.html',{'expensive_books':expensive_books})

def profile(request):
    return render(request, 'profile.html')
