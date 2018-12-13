from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from simple_posts_accounts.forms import UserRegistrationForm, ProfileEditForm, UserEditForm
from simple_posts_accounts.models import Profile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from simple_posts_accounts.models import Contact
from django.http import JsonResponse
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from actions.utils import create_action
from actions.models import Action

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'user_list.html', {'section': 'people', 'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'user_detail.html', {'section': 'people', 'user': user})

@login_required
def dashboard(request, action_id = None, user_id = None):
    # Display all actions if user does not follow other users
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    # Display only actions of people which users follow if they indeed follow other users
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    if user_id and action_id:
        actions = actions.exclude(id = action_id)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'dashboard.html', {'section': 'dashboard', 'actions': actions})

def register(request):
    if request.method == 'GET':
        user_form = UserRegistrationForm()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # We don't save immediately
            new_user = user_form.save(commit=False)
            # We instead set the password first with the 'set_password' method for proper encryption.
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # We have to associate each new user with an empty profile that can be edited later
            Profile.objects.create(user=new_user)
            create_action(new_user, 'created a new account')
            return render(request, 'register_done.html', {'new_user': new_user})
    return render(request, 'register.html', {'user_form': user_form})


@login_required
def edit_profile(request):
    if request.method == 'GET':
        user_edit_form = UserEditForm(instance=request.user)
        profile_edit_form = ProfileEditForm(instance=request.user.profile)
    if request.method == 'POST':
        user_edit_form = UserEditForm(instance=request.user, data=request.POST)
        profile_edit_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
            create_action(request.user, 'updated his profile')
            messages.success(request, 'Profile updated successfully')
            return render(request, 'dashboard.html')
        else:
            messages.error(request, 'Failed to update profile')
    return render(request, 'edit_profile.html', {'user_edit_form': user_edit_form, 'profile_edit_form': profile_edit_form})

@login_required
def follow_user(request, user_id):
    user = User.objects.get(id=user_id)
    Contact.objects.get_or_create(user_from=request.user, user_to=user)
    create_action(request.user, 'follows: ', user)
    return redirect(user)

@login_required
def unfollow_user(request, user_id):
    user = User.objects.get(id=user_id)
    Contact.objects.filter(user_from=request.user, user_to=user).delete()
    create_action(request.user, 'unfollowed: ', user)
    return redirect(user)
