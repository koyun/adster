from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField(default='')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='child')

    def __unicode__(self):
        p_list = self._recurse_for_parents(self)
        p_list.append(self.name)
        return self.get_separator().join(p_list)

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p.name)
            more = self._recurse_for_parents(p)
            p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def get_separator(self):
        return ' :: '

    @models.permalink
    def get_absolute_url(self):
        return ('category_index', (), { 'category': self.slug })


class Ad(models.Model):
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField(blank= True,null=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=140)
    description = models.CharField(max_length=140, blank=True, null=True)
    price = models.DecimalField(max_digits=9,decimal_places=2,blank=True,null=True)
    is_for_sale = models.BooleanField(default=True)


    def __unicode__(self):
        return self.title

class AdImage(models.Model):
    ad = models.ForeignKey(Ad)
    file_field = models.ImageField(upload_to='uploads/', blank=True)

