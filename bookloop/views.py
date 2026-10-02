from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, BookForm
from .models import Book, Profile


# REGISTER
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# LOGIN
def user_login(request):
    form = AuthenticationForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('book_list')
    return render(request, 'login.html', {'form': form})


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')


# VIEW BOOKS (BUYBRO + SELLBRO)
def book_list(request):
    books = Book.objects.filter(is_sold=False)
    return render(request, 'book_list.html', {'books': books})


# CREATE (SELLBRO ONLY)
@login_required
def book_create(request):
    if request.user.profile.role != 'sellbro':
        return redirect('book_list')

    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save(commit=False)
        book.sellbro = request.user
        book.save()
        return redirect('book_list')

    return render(request, 'book_form.html', {'form': form})


# UPDATE (ONLY OWNER SELLBRO)
@login_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.user != book.sellbro:
        return redirect('book_list')

    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')

    return render(request, 'book_form.html', {'form': form})


# DELETE (ONLY OWNER SELLBRO)
@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.user == book.sellbro:
        book.delete()

    return redirect('book_list')