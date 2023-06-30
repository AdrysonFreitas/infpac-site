from django.db import models
from django.db.models import Avg, Count, IntegerField
from django_resized import ResizedImageField
from django.utils.text import slugify
from django_cryptography.fields import encrypt
import time

class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome", unique=True)
    description = models.TextField(verbose_name="Descrição", blank=True)
    count_bulletins = models.IntegerField(default=0)
    slug = models.SlugField(max_length=100, null=True)

    @property
    def count_bulletins(self):
        return self.bulletins.aggregate(count_bulletins=Count('id'))['count_bulletins']

    class Meta:
        ordering = ['name']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super(Category, self).save(*args, **kwargs)

class Bulletin(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    image = ResizedImageField(size=[1920, 2714], verbose_name="Imagem", upload_to="img/bulletins/", help_text="Formato: 1920x2714")
    description = models.TextField(verbose_name="Descrição", blank=True)
    category = models.ForeignKey(Category,
        on_delete=models.CASCADE,
        related_name='bulletins', verbose_name="Categoria")
    views = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    bulletin_url = models.URLField(max_length=300, blank=True, verbose_name="URL do Arquivo", help_text="Link do arquivo no Google Drive")
    created_at = models.DateTimeField(verbose_name="Data de Publicação")
    slug = models.SlugField(max_length=200, null=True)

    def tag_list(self):
        tag_list = []
        for a in self.tags.all():
            tag_list.append(a.name)
        return tag_list
    tag_list.short_description = "Tags"

    def serialize(self):
        return {
            "id": self.id, 
            "name": self.username,
            "image": self.image,
            "category": self.category.name,
            "views": self.views,
            "tags": self.tag_list,
            "bulletin_url": self.bulletin_url
	}
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'boletim'
        verbose_name_plural = 'boletins'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "d/%i/%s/%s/" % (self.id, self.category.slug, self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        return super(Bulletin, self).save(*args, **kwargs)

class TeamMember(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    function = models.CharField(max_length=200, verbose_name="Função")
    link = models.CharField(max_length=200, verbose_name="Lattes")
    image = ResizedImageField(size=[300, 300], quality=100, verbose_name="Foto", upload_to="img/team/", help_text="Formato: 300x300", blank=True, default='img/team/default.png')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'membro'
        verbose_name_plural = 'equipe'

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    image = ResizedImageField(size=[300, 300], quality=100, verbose_name="Imagem", upload_to="img/partner/", help_text="Formato: 300x300", blank=True, default='img/partner/default.png')

    class Meta:
        ordering = ['name']
        verbose_name = 'colaborador'
        verbose_name_plural = 'colaboradores'

    def __str__(self):
        return self.name
 
class Action(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome")
    image = ResizedImageField(quality=100, verbose_name="Foto", upload_to="img/action/", default='img/action/default.png')

    class Meta:
        ordering = ['name']
        verbose_name = 'ação'
        verbose_name_plural = 'ações'

    def __str__(self):
        return self.name

class Subscribers(models.Model):
    email = models.CharField(unique=True, max_length=100, null=False)
    name = models.CharField(max_length=50)
    subscription_token = encrypt(models.CharField(max_length=50, unique=True, null=False))

    class Meta:
        ordering = ['name']
        verbose_name = 'inscrito'
        verbose_name_plural = 'inscritos'

    def __str__(self):
        return f'Inscrito de ID: {self.id}'

    def save(self, *args, **kwargs):
        self.subscription_token = f"{self.email}#{time.time()}"
        return super(Subscribers, self).save(*args, **kwargs)