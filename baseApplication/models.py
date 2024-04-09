from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#################-USERSTBL-###################

class UsersTBLManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UsersTBL(AbstractBaseUser):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(max_length=70, unique=True)
    phone_number = models.CharField(max_length=30)
    account_type = models.CharField(max_length=50)
    profile_picture = models.BinaryField(null=True, blank=True)
    bio_description = models.TextField()
    last_login = models.DateTimeField(null=True, blank=True)
    
    # New field added here
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    objects = UsersTBLManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # You can add more fields here if needed

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

#################-INFLUENCERSTBL-###################

class InfluencersTBL(models.Model):
    influencer_id = models.AutoField(primary_key=True)
    content_category = models.CharField(max_length=100)
    youtube_url = models.CharField(max_length=255, unique=True)
    facebook_url = models.CharField(max_length=255, unique=True)
    instagram_url = models.CharField(max_length=255, unique=True)
    tiktok_url = models.CharField(max_length=255, unique=True)
    twitter_url = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'InfluencersTBL'

#################-SPONSORSTBL-###################

class SponsorsTBL(models.Model):
    sponsor_id = models.AutoField(primary_key=True)
    content_category = models.CharField(max_length=100)
    sponsor_website = models.CharField(max_length=100)

    class Meta:
        db_table = 'SponsorsTBL'

#################-MESSAGESTBL-###################

class MessagingTBL(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    message_content = models.TextField()
    message_time = models.DateTimeField()

    class Meta:
        db_table = 'MessagingTBL'

#################-ADMINTBL-###################

class AdminsTBL(models.Model):
    admin_id = models.AutoField(primary_key=True)
    action_type = models.CharField(max_length=100)

    class Meta:
        db_table = 'AdminsTBL'

#################-YOUTUBETBL-###################

class YouTubeTBL(models.Model):
    youtube_id = models.AutoField(primary_key=True)
    youtube_url = models.CharField(max_length=255, unique=True)
    average_views = models.IntegerField()
    average_engagement = models.IntegerField()
    average_likes = models.IntegerField()
    subscribers_count = models.IntegerField()
    last_post_date = models.DateTimeField()

    class Meta:
        db_table = 'YouTubeTBL'

#################-FACEBOOKTBL-###################

class FacebookTBL(models.Model):
    facebook_id = models.AutoField(primary_key=True)
    facebook_url = models.CharField(max_length=255, unique=True)
    average_views = models.IntegerField()
    average_engagement = models.IntegerField()
    average_likes = models.IntegerField()
    subscribers_count = models.IntegerField()
    last_post_date = models.DateTimeField()

    class Meta:
        db_table = 'FacebookTBL'

#################-INSTAGRAMTBL-###################

class InstagramTBL(models.Model):
    instagram_id = models.AutoField(primary_key=True)
    instagram_url = models.CharField(max_length=255, unique=True)
    average_views = models.IntegerField()
    average_engagement = models.IntegerField()
    average_likes = models.IntegerField()
    subscribers_count = models.IntegerField()
    last_post_date = models.DateTimeField()

    class Meta:
        db_table = 'InstagramTBL'

#################-TIKTOKTBL-###################

class TiktokTBL(models.Model):
    tiktok_id = models.AutoField(primary_key=True)
    tiktok_url = models.CharField(max_length=255, unique=True)
    average_views = models.IntegerField()
    average_engagement = models.IntegerField()
    average_likes = models.IntegerField()
    subscribers_count = models.IntegerField()
    last_post_date = models.DateTimeField()

    class Meta:
        db_table = 'TiktokTBL'

#################-TWITTERTBL-###################

class TwitterTBL(models.Model):
    twitter_id = models.AutoField(primary_key=True)
    twitter_url = models.CharField(max_length=255, unique=True)
    average_views = models.IntegerField()
    average_engagement = models.IntegerField()
    average_likes = models.IntegerField()
    subscribers_count = models.IntegerField()
    last_post_date = models.DateTimeField()

    class Meta:
        db_table = 'TwitterTBL'