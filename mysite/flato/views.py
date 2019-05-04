from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
import json, requests
from django.template import loader
from .models import News, Movie
from django.views.generic import ListView, DetailView, TemplateView
from .scraper import GeneralNews, Movies, TechNews, ScienceNews, BusinessNews, GamingNews, SportNews , PoliticalNews
from django.db.models import Q
from .forms import SignUpForm
from datetime import datetime, timedelta
from django.conf import settings

'''
Main view for the /feed
'''
class MultipleModelView(TemplateView):
    template_name = 'feed.html'

    def get_context_data(self, **kwargs):


        context = super(MultipleModelView, self).get_context_data(**kwargs)
        general = self.request.user.profile.chip_general
        business = self.request.user.profile.chip_business
        politics = self.request.user.profile.chip_politics
        sport = self.request.user.profile.chip_sport
        gaming = self.request.user.profile.chip_gaming
        technology = self.request.user.profile.chip_technology

        Qgeneral = Q()
        Qbusiness = Q()
        Qpolitics = Q()
        Qsport = Q()
        Qgaming = Q()
        Qtechnology = Q()
        Qtitle = Q()
        Qauthor = Q()

        Qdescription = Q()
        Qtime = Q()
        try:
            Qnewsnumber = self.request.session['newsnumber']
        except:
            Qnewsnumber = 15

        try:
            Qtitle = Q(title__contains=str(self.request.session['title']))
        except:
            Qtitle = Q()

        try:
            Qdescription = Q(description__contains=self.request.session['description'])
        except:
            Qdescription = Q()

        try:
            Qauthor = Q(author__contains=self.request.session['author'] )
        except:
            Qauthor = Q()

        try:
            Qtime = Q(time=self.request.session['time'])
        except:
            Qtime = Q()

        if general == "True":
            Qgeneral = Q(tag="General")
        if business == "True":
            Qbusiness = Q(tag="Business")
        if politics == "True":
            Qpolitics = Q(tag="Politics")
        if sport == "True":
            Qsport = Q(tag="Sport")
        if gaming == "True":
            Qgaming = Q(tag="Gaming")
        if technology == "True":
            Qtechnology = Q(tag="Technology ")



        context['newslist'] = News.objects.filter(
            (Qgeneral|
            Qbusiness|
            Qpolitics|
            Qsport|
            Qgaming|
            Qtechnology)&
            Qtitle&
            Qdescription&
            Qauthor
        ).order_by("-date")[:int(Qnewsnumber)]

        context['general'] = self.request.user.profile.chip_general
        context['business'] = self.request.user.profile.chip_business
        context['politics'] = self.request.user.profile.chip_politics
        context['sport'] = self.request.user.profile.chip_sport
        context['gaming'] = self.request.user.profile.chip_gaming
        context['technology'] = self.request.user.profile.chip_technology
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'news.html'

class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie.html'

'''
Handle adding a chip
'''
def addchip(request):
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.id)
        data = request.GET.get('chip', None)
        if data.lower() == "general":
            user.profile.chip_general = "True"
        if data.lower() == "business":
            user.profile.chip_business = "True"
        if data.lower() == "politics":
            user.profile.chip_politics = "True"
        if data.lower() == "sport":
            user.profile.chip_sport = "True"
        if data.lower() == "gaming":
            user.profile.chip_gaming = "True"
        if data.lower() == "technology":
            user.profile.chip_technology = "True"
        user.save()
        return redirect('/feedupdate', permanent=True)


'''
Handle deleting a chip
'''
def deletechip(request):
    if request.method == 'GET':
        user = User.objects.get(pk=request.user.id)
        data = request.GET.get('chip', None)
        if data.lower() == "general":
            user.profile.chip_general = "False"
        if data.lower() == "business":
            user.profile.chip_business = "False"
        if data.lower() == "politics":
            user.profile.chip_politics = "False"
        if data.lower() == "sport":
            user.profile.chip_sport = "False"
        if data.lower() == "gaming":
            user.profile.chip_gaming = "False"
        if data.lower() == "technology":
            user.profile.chip_technology = "False"

        user.save()
        return redirect('/feed')

    return HttpResponse("test")

'''
Handle search function
'''
def search(request):
    if request.method == 'POST':
        newsnumber = request.POST.get("newsnumber")
        title  = request.POST.get("title")
        description = request.POST.get("description")
        author = request.POST.get("author")
        time = request.POST.get("time")
        request.session['newsnumber'] = newsnumber
        request.session['title'] = title
        request.session['description'] = description
        request.session['author'] = author
        request.session['time'] = time
        return redirect ('/feed')


'''
Handle clearing the search function
'''
def clear(request):
    if request.method == 'POST':
        del request.session['newsnumber']
        del request.session['title']
        del request.session['description']
        del request.session['author']
        del request.session['time']
        return redirect ('/feed')

def index(request):

    if request.user.is_authenticated():
                template = loader.get_template('index.html')
                context = {
                    'images' : "[test,fsdfseff]"
                }
                return HttpResponse(template.render(context, request))

    else:
        return redirect('/login/')

def update(request):

    print('Last database update:' + settings.LATEST_UPDATE)

    try:
        GeneralNews(settings.LATEST_UPDATE)
    except:
        print("BBC News Error")
    try:
        BusinessNews(settings.LATEST_UPDATE)
    except:
        print("Business News Error")
    try:
        TechNews(settings.LATEST_UPDATE)
    except:
        print("Tech News Error")
    try:
        ScienceNews(settings.LATEST_UPDATE)
    except:
        print("Tech News Error")
    try:
        GamingNews(settings.LATEST_UPDATE)
    except:
        print("Gaming News Error")
    try:
        SportNews(settings.LATEST_UPDATE)
    except:
        print("Sport News Error")
    try:
        PoliticalNews(settings.LATEST_UPDATE)
    except:
        print("Political News Error")

    settings.LATEST_UPDATE = str(datetime.now() + timedelta(hours=-1))
    print('Updated Database at:' + settings.LATEST_UPDATE)

    return redirect('/feed')

def updatedb(request):
    print('Last database update:' + settings.LATEST_UPDATE)

    try:
        GeneralNews(settings.LATEST_UPDATE)
    except:
        print("BBC News Error")
    try:
        BusinessNews(settings.LATEST_UPDATE)
    except:
        print("Business News Error")
    try:
        TechNews(settings.LATEST_UPDATE)
    except:
        print("Tech News Error")
    try:
        ScienceNews(settings.LATEST_UPDATE)
    except:
        print("Tech News Error")
    try:
        GamingNews(settings.LATEST_UPDATE)
    except:
        print("Gaming News Error")
    try:
        SportNews(settings.LATEST_UPDATE)
    except:
        print("Sport News Error")
    try:
        PoliticalNews(settings.LATEST_UPDATE)
    except:
        print("Political News Error")


    settings.LATEST_UPDATE = str(datetime.now() + timedelta(hours=-1))
    print('Updated Database anonymously at:' + settings.LATEST_UPDATE)
    return HttpResponse("Updated Database anonymously")

'''
Handle sign up
'''
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('news_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
