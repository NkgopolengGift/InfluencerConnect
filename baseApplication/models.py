from django.db import models
from django.utils import timezone

# Create your models here.
#############################################################S
class UsersTBL(models.Model):
    username = models.CharField(max_length=70)
    email = models.EmailField(max_length=70)
    phone_number = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    account_type = models.CharField(max_length=50)
    profile_picture = models.BinaryField(null=True, blank=True)
    bio_description = models.TextField()
    last_login = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.last_login:
            self.last_login = timezone.now()
        super(UsersTBL, self).save(*args, **kwargs)
#################################################################################
class InfluencersTBL(models.Model):
    content_category = models.CharField(max_length=50)
    average_views = models.IntegerField()
    average_engagement = models.IntegerField()
    average_likes = models.IntegerField()
    subscribers_count = models.IntegerField()
    last_update = models.DateTimeField()
    youtube_url = models.URLField(unique=True)
    facebook_url = models.URLField(unique=True)
    instagram_url = models.URLField(unique=True)
    tiktok_url = models.URLField(unique=True)
    twitter_url = models.URLField(unique=True)

class SponsorsTBL(models.Model):
    company_name = models.CharField(max_length=50)
    content_category = models.CharField(max_length=50)
    company_website = models.URLField(max_length=50)

class MessagingTBL(models.Model):
    sender = models.ForeignKey(UsersTBL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UsersTBL, on_delete=models.CASCADE, related_name='received_messages')
    message_content = models.TextField()
    message_time = models.DateTimeField()

class AdminsTBL(models.Model):
    admin = models.ForeignKey(UsersTBL, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=50)

class YouTubeTBL(models.Model):
    influencer = models.OneToOneField(InfluencersTBL, on_delete=models.CASCADE)
    account_url = models.URLField(unique=True)

class FacebookTBL(models.Model):
    influencer = models.OneToOneField(InfluencersTBL, on_delete=models.CASCADE)
    account_url = models.URLField(unique=True)

class InstagramTBL(models.Model):
    influencer = models.OneToOneField(InfluencersTBL, on_delete=models.CASCADE)
    account_url = models.URLField(unique=True)

class TiktokTBL(models.Model):
    influencer = models.OneToOneField(InfluencersTBL, on_delete=models.CASCADE)
    account_url = models.URLField(unique=True)

class TwitterTBL(models.Model):
    influencer = models.OneToOneField(InfluencersTBL, on_delete=models.CASCADE)
    account_url = models.URLField(unique=True)

