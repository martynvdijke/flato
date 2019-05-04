from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from autoslug import AutoSlugField


##store data wich belongs to the user itself
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wheater_city = models.CharField(max_length=200, default="Eindhoven")
    wheater_degree = models.CharField(max_length=10, default="celsius")
    wheater_citykey = models.TextField(null=True, blank=True)
    wheater_country = models.TextField(null=True, blank=True)
    wheater_province = models.TextField(null=True, blank=True)
    wheater_dailyforecasts = models.TextField(null=True, blank=True)
    wheater_today = models.TextField(null=True, blank=True)
    chip_general = models.TextField(null=True, blank=True, default="True")
    chip_sport = models.TextField(null=True, blank=True, default="True")
    chip_business = models.TextField(null=True, blank=True, default="True")
    chip_technology = models.TextField(null=True, blank=True, default="True")
    chip_politics = models.TextField(null=True, blank=True, default="True")
    chip_gaming = models.TextField(null=True, blank=True, default="True")
    numberofitems = models. IntegerField(null=True, blank=True, default=15)


## create extended user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


## save extended user profile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

## news model
class News(models.Model):
    source = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    author = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # set the slug explicitly
        super(News, self).save(*args, **kwargs)  # call Django's save()


class Movie(models.Model):
    title = models.TextField(null=True, blank=True)
    vote_count = models.TextField(null=True, blank=True)
    vote_average = models.TextField(null=True, blank=True)
    poster_path = models.TextField(null=True, blank=True)
    gerne_ids = models.TextField(null=True, blank=True)
    backdrop_path = models.TextField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    popularity = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)  # set the slug explicitly
        super(Movie, self).save(*args, **kwargs)  # call Django's save()
