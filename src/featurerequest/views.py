from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import LoginForm, FeatureForm
from .models import Features


@login_required
def index(request, page=1):
    """
    It displays list of feature requests. 10 records will be displayed per page in descending order of target_date.
    :param request: HttpRequest object provided by django engine.
    :param page: the page number that needs to be displayed.

    """
    latest_feature_list = Features.objects.filter().order_by('-target_date')
    paginator = Paginator(latest_feature_list, 10)

    try:
        feature_list = paginator.page(page)
    except PageNotAnInteger:
        feature_list = paginator.page(1)  # show first page if page is not PageNotAnInteger
    except EmptyPage:
        feature_list = paginator.page(paginator.num_pages)

    startPoint = 1
    endPoint = feature_list.paginator.num_pages

    if feature_list.paginator.num_pages > 10:
        if feature_list.number < 6:
            startPoint = 1
            endPoint = 10
        elif feature_list.number + 4 >= feature_list.paginator.num_pages:
            startPoint = feature_list.paginator.num_pages - 9
            endPoint = feature_list.paginator.num_pages
        else:
            startPoint = feature_list.number - 5
            endPoint = feature_list.number + 4

    pageList = range(startPoint, endPoint + 1)

    return render(request, 'featurerequest/index.html', {'feature_list': feature_list, 'pageList': pageList})


@login_required
def add_features(request):
    """
    Creates Feature Request on POST.
    Blank form will be rendered on GET.

    """
    feature_form = FeatureForm(request.POST or None)
    if request.method == 'POST':
        if feature_form.is_valid():
            feature_form.save()
            messages.success(request, 'The Feature request was successfully created!.')
            return redirect('/features/')
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'featurerequest/addfeatures.html', {'feature_form': feature_form})
    else:
        feature_form = FeatureForm()
        return render(request, 'featurerequest/addfeatures.html', {'feature_form': feature_form})


def userlogin(request):
    """
    Blank login form will be rendered on GET
    User will be logged in and redirected to Features page on providing valid credentials.

    """
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/features/')
    return render(request, 'featurerequest/login.html', {'login_form': form})


def userlogout(request):
    """
    User will be logged out.
    """
    logout(request)
    return redirect('/features/')
