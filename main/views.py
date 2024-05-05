from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Post, LikePost, followersCount
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.
@login_required(login_url='login')
def home_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = followersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames).order_by('-created_on')
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    all_users =User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.filter(username=user.user)
        user_following_all.append(user_list)

    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestion_username_profile_list = list(chain(*username_profile_list))

    context = {'user_profile': user_profile, 'posts': feed_list, 'suggestion_username_profile_list': suggestion_username_profile_list[:4]}
    return render(request, 'main/index.html', context) 

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('conf_password')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'This email already exists, please change the email address')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists, please change the username')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model , id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Passwords are not the same')
            return redirect('register')
    else:    
        return render(request, 'main/register1.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('passcode')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'main/login.html')
    
@login_required(login_url='login')
def profile_view(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_len = len(user_post)

    follower = request.user.username
    user = pk
    if followersCount.objects.filter(user=user, follower=follower).first():
        button_text = 'Ne plus suivre'
    else:
        button_text = 'Suivre'

    user_followers = len(followersCount.objects.filter(user=pk))
    user_following = len(followersCount.objects.filter(follower=pk))

    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_post': user_post,
        'user_post_len': user_post_len,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'main/profil.html', context)
    
@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def settings_view(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.profileimg
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        else:
            image = request.FILES.get('image')
            bio = request.POST.get('bio')
            location = request.POST.get('location')

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')
    return render(request, 'main/setts.html', context={'user_profile': user_profile})

@login_required(login_url='login')
def upload_view(request):
    if request.method == 'POST':
        user = request.user.username
        caption = request.POST.get('caption')
        image = request.FILES.get('image_upload')

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('home')
    else:
        return render(request, 'main/upload')
    
@login_required(login_url='login')
def like_view(request):  
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(username=username, post_id=post_id).first()

    if like_filter is None:
        new_like = LikePost.objects.create(username=username, post_id=post_id)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('home') 
    else:
        like_filter.delete() 
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('home')
    

@login_required(login_url='login')
def follow_view(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        user = request.POST.get('user')

        if followersCount.objects.filter(user=user, follower=follower).first():
            delete_followers = followersCount.objects.filter(user=user, follower=follower)
            delete_followers.delete()
            return redirect('/profile/'+user)
        else:
            new_followers = followersCount.objects.create(user=user, follower=follower)
            new_followers.save()
            return redirect('/profile/'+user)
    else:
        return redirect('home')
    
@login_required(login_url='login')
def search_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        username = request.POST.get('username')
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

    return render(request, 'main/search.html', context={'user_profile': user_profile, 'username_profile_list': username_profile_list})