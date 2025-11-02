from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import PageForm
from .models import Page
from datetime import datetime
from zoneinfo import ZoneInfo
from django.contrib.auth import get_user_model

def create_admin_user(request):
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "password123")
        return HttpResponse("✅ Superuser created!")
    else:
        return HttpResponse("⚠️ Admin user already exists.")

class IndexView(View):
    def get(self, request):
        datetime_now = datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("%_Y年%m月%d日 %H:%M:%S")
        return render(request, "tabemory/index.html",{"datetime_now" : datetime_now})
    
    
class PageCreateView(View):
    def get(self, request):
        form = PageForm()
        return render(request, "tabemory/page_form.html", {"form" : form})
    
    def post(self, request):
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("tabemory:index")
        return render(request, "tabemory/page_form.html", {"form" : form})
    

class PageListView(View):
    def get(self,request):
        page_list = Page.objects.all()
        return render(request, "tabemory/page_list.html", {"page_list" : page_list})

class PageDetailView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        return render(request, "tabemory/page_detail.html", {"page" : page})
    
class PageUpdateView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        form = PageForm(instance = page)
        return render(request, "tabemory/page_update.html", {"form" : form})
    
    def post(self, request, id):
        page = get_object_or_404(Page, id=id)
        form = PageForm(request.POST, request.FILES, instance = page)
        if form.is_valid():
            form.save()
            return redirect("tabemory:page_detail", id = id)
        return render(request, "tabemory/page_form.html", {"form" : form})
    
class PageDeleteView(View):
    def get(self, request, id):
        page = get_object_or_404(Page, id = id)
        return render(request, "tabemory/page_confirm_delete.html", {"page" : page})
    
    def post(self, request, id):
        page = get_object_or_404(Page, id = id)
        page.delete()
        return redirect("tabemory:page_list")
        

index = IndexView.as_view()
page_create = PageCreateView.as_view()
page_list = PageListView.as_view()
page_detail = PageDetailView.as_view()
page_update =  PageUpdateView.as_view()
page_delete = PageDeleteView.as_view()
