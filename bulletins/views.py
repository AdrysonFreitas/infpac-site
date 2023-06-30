from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .models import Tag,Category,Bulletin,TeamMember,Partner,Action,Subscribers
from django.template import loader
from django.views import generic
from django.views.generic.edit import FormView
from django.urls import reverse
from django.db.models import Avg, IntegerField
from django.db.models.functions import Round, Cast
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
from django.core.mail import send_mail,EmailMessage,send_mass_mail,get_connection, EmailMultiAlternatives
from django.contrib import messages
from .forms import NewsletterCreatorForm
from django.conf import settings
from .static.bulletins.assets import blocked_emails
from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from .utils.encryption_util import *
from django.utils.html import strip_tags, format_html
import random
import re
import logging
import traceback
import sys
import pdb

import json

def send_bulk_email(request, subscribers, subject, template, from_email):
    emails = []
    for recipient in subscribers:
        token = encrypt(recipient.subscription_token)
        unsubscribe_url = request.build_absolute_uri(
                reverse('unsubscribe')) + "?token=" + token

        context = Context({ 'name': recipient.name,
                    'unsubscribe_url': unsubscribe_url })

        html_content = template.render(context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, from_email, [recipient.email])
        email.attach_alternative(html_content, "text/html")
        emails.append(email)
    connection = get_connection()
    return connection.send_messages(emails)

def add_click(request):
    bulletin_id = request.GET.get("bulletinId", None)

    bulletin = Bulletin.objects.get(pk=bulletin_id)
    bulletin.views = bulletin.views + 1
    bulletin.save()

    return HttpResponse("Hit added.")

def validateEmail(request): 
    disposable_emails = blocked_emails.disposable_emails()
    email = request.POST.get("email", None)   
    if email == "":
        res = JsonResponse({'msg': 'E-mail é obrigatório.'})
    elif Subscribers.objects.filter(email = email):
        res = JsonResponse({'msg': 'E-mail já cadastrado.'})
    elif not re.search(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        res = JsonResponse({'msg': 'E-mail inválido.'})
    elif email.split('@')[-1] in disposable_emails:
        res = JsonResponse({'msg': 'E-mails temporários não são permitidos.'})
    else:
        res = JsonResponse({'msg': 'Valid'})
    return res

def validateName(request): 
    name = request.POST.get("name", None)   
    if name == "":
        res = JsonResponse({'msg': 'Nome é obrigatório.'})
    else:
        res = JsonResponse({'msg': 'Valid'})
    return res

def newsletter(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        name = post_data.get("name", None)
        if re.search(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
            subscribers = Subscribers()
            subscribers.email = email
            subscribers.name = name
            subscribers.save()

            token = encrypt(subscribers.subscription_token)
            #pdb.set_trace()

            unsubscribe_url = request.build_absolute_uri(
                reverse('unsubscribe')) + "?token=" + token

            welcome_msg = get_template('bulletins/emails/welcome_message.txt')
            html_welcome_msg = get_template('bulletins/emails/html_welcome_message.html')

            data = { 'name': name,
                     'unsubscribe_url': unsubscribe_url }

            subject = 'Confirmada a inscrição nas atualizações informativas do Infpac!'
            message = welcome_msg.render(data)
            html_message = html_welcome_msg.render(data)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, f"Infpac <{email_from}>", recipient_list, html_message=html_message)

            res = JsonResponse({'msg': 'Obrigado. Inscrição feita com sucesso!'})
            return res
        else:
            res = JsonResponse({'msg': 'Erro'})
            return res
    return render(request, 'bulletins/newsletter.html')

class IndexView(generic.ListView):
    model: Bulletin
    template_name = 'bulletins/index.html'
    context_object_name = 'latest_bulletin_list'
    paginate_by = 9

    def get_queryset(self):
        try:
            latest = Bulletin.objects.latest('id')
        except Bulletin.DoesNotExist:
            latest = Bulletin.objects.none()
        bulletin_list = Bulletin.objects.order_by('-id')

        query = self.request.GET.get('q')
        if query:
            bulletin_list = Bulletin.objects.filter(name__icontains=query)
        else:
            bulletin_list = Bulletin.objects.order_by('-id')
        return bulletin_list

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            context['latest'] = Bulletin.objects.latest('id')
        except Bulletin.DoesNotExist:
            context['latest'] = Bulletin.objects.none()
        return context

class BulletinDetailView(generic.DetailView):
    model = Bulletin
    template_name = 'bulletins/bulletin.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(BulletinDetailView, self).get_context_data(**kwargs)
        return context

class CategoryIndexView(generic.ListView):
    model = Category
    template_name = 'bulletins/category_index.html'
    context_object_name = 'latest_category_list'
    paginate_by = 9

    def get_queryset(self):
        category_list = Category.objects.order_by('name')

        query = self.request.GET.get('q')
        if query:
            category_list = Category.objects.filter(name__icontains=query)
        else:
            category_list = Category.objects.order_by('name')
        return category_list

    def get_context_data(self, **kwargs):
        context = super(CategoryIndexView, self).get_context_data(**kwargs)
        items = list(Category.objects.all())
        context['random_category'] = random.choice(items)
        return context

class CategoryDetailView(generic.DetailView):
    model = Category
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        published_bulletins = self.get_published_bulletins()
        context['most_viewed'] = sorted(Bulletin.objects.filter(category=self.get_object()), key=lambda m: m.views, reverse=True)[:5]
        context['published_bulletins'] = published_bulletins
        context['page_obj'] = published_bulletins

        return context

    def get_published_bulletins(self):
        queryset = self.object.bulletins.all() 
        paginator = Paginator(queryset,10) #paginate_by
        page = self.request.GET.get('page')
        published_bulletins = paginator.get_page(page)
        return published_bulletins

    template_name = 'bulletins/category.html'

class TeamIndexView(generic.ListView):
    model: TeamMember
    template_name = 'bulletins/team.html'
    context_object_name = 'latest_team_list'

    def get_queryset(self):
        team_list = TeamMember.objects.order_by('name')
        return team_list

    def get_context_data(self, **kwargs):
        context = super(TeamIndexView, self).get_context_data(**kwargs)
        return context

class PartnersIndexView(generic.ListView):
    model: Partner
    template_name = 'bulletins/partners.html'
    context_object_name = 'latest_partner_list'

    def get_queryset(self):
        partners_list = Partner.objects.order_by('name')
        return partners_list

    def get_context_data(self, **kwargs):
        context = super(PartnersIndexView, self).get_context_data(**kwargs)
        return context

class ActionIndexView(generic.ListView):
    model: Action
    template_name = 'bulletins/actions.html'
    context_object_name = 'latest_action_list'

    def get_queryset(self):
        action_list = Action.objects.order_by('name')
        return action_list

    def get_context_data(self, **kwargs):
        context = super(ActionIndexView, self).get_context_data(**kwargs)
        return context

class newsletterCreator(FormView):
    template_name = "bulletins/newslettercreator.html"
    form_class = NewsletterCreatorForm
    success_url = "/admin/criar-newsletter/"

    def form_valid(self, form):
        subject = form.cleaned_data.get('subject')
        template = Template(form.cleaned_data.get('message'))
        subscribers = Subscribers.objects.all()
        #pdb.set_trace()

        mail = send_bulk_email(self.request, subscribers, subject, template, from_email=f"Infpac <{settings.EMAIL_HOST_USER}>")

        if mail:
            messages.success(self.request, "E-mail enviado com sucesso!")
        else:
            messages.error(self.request, "Houve um erro ao enviar o e-mail")

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial_msg = get_template('bulletins/emails/default_newsletter.html')
        
        initial['subject'] = 'Mensagem do Infpac'
        initial['receivers'] = ','.join([active.email for active in Subscribers.objects.all()])
        initial['message'] = initial_msg.render

        return initial

def unsubscribe(request):
    if "POST" == request.method:
        raise Http404

    token = request.GET.get("token", None)
    token = decrypt(token)
    #pdb.set_trace()

    if token:
        token = token.split("#")
        email = token[0]
        print(email)
        initiate_time = token[1]  # time when email was sent , in epoch format. can be used for later calculations
        try:
            Subscribers.objects.get(email=email).delete()
            messages.success(request, "Inscrição cancelada. Obrigado!")
        except ObjectDoesNotExist as e:
            logging.getLogger("warning").warning(traceback.format_exc())
            messages.error(request, "Link inválido")
    else:
        logging.getLogger("warning").warning("Invalid token ")
        messages.error(request, "Link inválido")

    return HttpResponseRedirect(reverse('index'))