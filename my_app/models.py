from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
class Artist(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    sort_title = models.CharField(max_length=255)
    is_artist = models.BooleanField(default=True)
    birth_date = models.IntegerField(null=True, blank=True)
    death_date = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "artists"
        ordering = ["sort_title"]

class Gallery(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    tgn_id = models.IntegerField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    number = models.CharField(max_length=50, blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

class Artwork(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField(null=True, blank=True)
    main_reference_number = models.CharField(max_length=50, null=True, blank=True)
    date_start = models.IntegerField(null=True, blank=True)
    date_end = models.IntegerField(null=True, blank=True)
    date_display = models.CharField(max_length=255, null=True, blank=True)
    date_qualifier_title = models.CharField(max_length=255, null=True, blank=True)
    artist_display = models.TextField(null=True, blank=True)
    place_of_origin = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    dimensions = models.TextField(null=True, blank=True)
    medium_display = models.TextField(null=True, blank=True)
    credit_line = models.TextField(null=True, blank=True)
    catalogue_display = models.TextField(null=True, blank=True)
    publication_history = models.TextField(null=True, blank=True)
    exhibition_history = models.TextField(null=True, blank=True)
    provenance_text = models.TextField(null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    is_public_domain = models.BooleanField(default=False, null=True, blank=True)
    copyright_notice = models.CharField(max_length=255, null=True, blank=True)
    is_on_view = models.BooleanField(default=False, null=True, blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True, blank=True)
    artwork_type_id = models.IntegerField(null=True, blank=True)
    department_id = models.CharField(max_length=50, null=True, blank=True)
    artist = models.ForeignKey(Artist, on_delete=models.SET_NULL, null=True, blank=True)
    style_id = models.CharField(max_length=255, null=True, blank=True)
    image_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)
