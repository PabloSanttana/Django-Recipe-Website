from django.shortcuts import render, redirect, get_object_or_404

from authors.forms import RegisterForm, LoginForm, RecipeForm, UpdadeUserForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from recipes.models import Recipe

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is create, please log in.')

        del(request.session['register_form_data'])
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })


def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
            return redirect('authors:dashboard')
        else:
            messages.error(request, 'Invalid credentials.')

    else:
        messages.error(request, 'Error to validate form data.')

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def profile_view(request):
    user = User.objects.get(username=request.user.username)
    form = UpdadeUserForm(
        request.POST or None,
        instance=user
    )

    if form.is_valid():
        form.save()
        messages.success(request, 'Edit with success.')
        return redirect('authors:profile')

    return render(request, 'authors/pages/dashboard_profile.html', context={
        'form': form,
        'title': 'Profile'
    })
    ...


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):

    return render(request, 'authors/pages/logout.html')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_user(request):
    if not request.POST:
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        return redirect('authors:login')

    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    # fazer paginacao dps
    recipes = Recipe.objects.filter(
        author__username=request.user.username, is_published=False).order_by('-id')
    return render(request, 'authors/pages/dashboard.html', context={
        'recipes': recipes,
        'title': 'Dashboard'
    })


# foi mudada para class baseada em view
""" @login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = get_object_or_404(
        Recipe, pk=id, is_published=False, author=request.user)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Edit with success.')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/pages/dashboard_recipes.html', context={
        'form': form,
        'title': 'Dashboard Recipe'
    })
 """

# foi mudada para class baseada em view
""" @login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Recipe create success')
        return redirect('authors:dashboard')

    return render(request, 'authors/pages/dashboard_recipes.html', context={
        'form': form,
        'title': 'Recipe Create',
    })
 """

# foi mudada para class baseada em view
""" 
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        return redirect('authors:dashboard')

    id = request.POST.get('id')
    recipe = get_object_or_404(
        Recipe, pk=id, is_published=False, author=request.user)

    recipe.delete()
    messages.success(request, 'Delete with success.')
    return redirect('authors:dashboard') """
