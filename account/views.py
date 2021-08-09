from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article, Category
from django.urls import reverse_lazy, resolve, reverse
from .models import User
from .forms import ProfileForm, SignUp
from django.contrib.auth.views import LoginView
from .mixin import FieldsSetterMixin, UpdateAccess, DeleteAccessMixin, SimpleUsersLimitation
# Django email sender
from django.core.mail import send_mail
import hashlib
import time
from Learning.settings import EMAIL_HOST_USER


# Create your views here.

# Listing Articles for user profile. This view is logged in protected
class ArticleList(SimpleUsersLimitation, ListView):
    template_name = 'AdminLTE/home.html'
    context_object_name = 'articles'

    def get_queryset(self):  # Defining desired queryset
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


# Creating Article view. To access this view, user should be logged in
class ArticleCreate(SimpleUsersLimitation, FieldsSetterMixin, CreateView):
    model = Article
    # Specify the intended fields to be filled out
    template_name = 'AdminLTE/Create_Update.html'


class ArticleUpdate(SimpleUsersLimitation, FieldsSetterMixin, UpdateAccess, UpdateView):
    model = Article
    # Specify the intended fields to be filled out
    template_name = 'AdminLTE/Create_Update.html'


class ArticleDelete(LoginRequiredMixin, DeleteAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('accounts:article_list')
    context_object_name = 'article'
    template_name = 'AdminLTE/Delete.html'


class ArticlePreview(UpdateAccess, DetailView):
    model = Article
    template_name = 'blog/post.html'


class Profile(LoginRequiredMixin, UpdateView):
    template_name = 'AdminLTE/Profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs


# We inherit from default login view to overwrite some changes
class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_author or user.is_superuser:
            return reverse_lazy("accounts:article_list")
        return reverse_lazy("accounts:profile")


def register(request):
    global form_obj
    # If the user requested from an explorer as GET method do this:
    if request.method == 'GET':
        # Create an instance of empty form to display to the user
        form_obj = SignUp()

    # If the user sent the request via forms or other POST method senders to this:
    elif request.method == 'POST':
        # Create an instance of form with the value sent via POST method
        form = SignUp(request.POST)

        # This method will call the validation methods in form and return
        # the form instance with cleaned_data if is valid and False if not
        if form.is_valid():
            # Save the form data but not into the database because we want to do some changes
            user = form.save(commit=False)
            # Deactivate the user
            user.is_active = False
            # Save the user
            user.save()

            pk = user.pk
            username = user.username
            email = user.email
            # Create the hash of user's username
            hashed = hashlib.sha256(username.upper().encode()).hexdigest()
            # Get the host name, here is 127.0.0.1:8000
            host = request.META['HTTP_HOST']
            curr_time = time.time()

            message = f"""
            Hi {username},
            We have emailed you from django-web developers
            Thanks for registering in out website.
            Here is your activation code
            http://{host}/activate/?u={pk}&se={hashed}&nw={curr_time}
            """

            send_mail('Activation Code', message, EMAIL_HOST_USER, [email, ], fail_silently=False)

            # Set a custom session in users browser and read or delete it whenever we want
            request.session['val_cd'] = pk

            # Redirect the user to activate page
            return redirect('activate')

        # If the form was not valid, display the form again with entered values
        form_obj = SignUp(request.POST)

    return render(request, 'registration/register.html', {'form': form_obj})


class Activation(View):

    def get(self, request):
        try:
            pk = request.GET['u']
            user = User.objects.get(pk=pk)
            hashed = request.GET['se']
            user_hashed = hashlib.sha256(user.username.upper().encode()).hexdigest()
            sent_time = float(request.GET['nw'])
            curr_time = time.time()
            output = None
            if (curr_time - sent_time) > 900:
                output = 'expired'
            elif user.is_active:
                output = 'active'
            elif hashed != user_hashed:
                output = 'invalid'
            if not output:
                output = 'done'
                user.is_active = True
                user.save()
            return render(request, 'registration/notify.html', {'output': output})

        except:
            if request.session.get('val_cd'):
                user = User.objects.get(pk=int(request.session.get('val_cd')))
                del request.session['val_cd']
                if user.is_active:
                    output = 'active'
                else:
                    output = 'not_active'

                return render(request, 'registration/notify.html', {'output': output})
            else:
                raise Http404

def test(request):
    print(request.session)
    request.session['username'] = 'AM80'
    print(request.session.get('username', 'None'))
    return HttpResponse('Done' + request.session['username'])
