from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import secrets

#################-USERSTBL-###################

class UserManager(BaseUserManager):
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

class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(max_length=70, unique=True)
    phone_number = models.CharField(max_length=30)
    account_type = models.CharField(max_length=15)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # New field added here
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    options={
                'ordering': ['user_id'],  # Explicitly set ordering if supported
            },
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

#################-INFLUENCERTBL-###################

class Influencer(models.Model):
    influencer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #username = models.CharField(max_length=100, unique=True)
    content_category = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

#################-SPONSORTBL-###################

class Sponsor(models.Model):
    sponser_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_category = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

#################-PLATFORMTBL-###################

class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=100)
    platform_url = models.CharField(max_length=200, unique=True)
    likes = models.IntegerField(default=0) 
    views = models.IntegerField(default=0) 
    subscribers = models.IntegerField(default=0)
    comments = models.IntegerField(default=0) 
    videos = models.IntegerField(default=0)

    def __str__(self):
        return self.platform_name
    
#################-Chat-###################
class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    sponser = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.influencer.user.username} and {self.sponsor.user.username} at {self.time}"

#################-Payment-###################

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=150, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    verified = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.amount}"
    
    def save(self, *args, **kwargs):
        while not self.reference:
            reference = secrets.token_urlsafe(50)
            object_with_similar_reference = Payment.objects.filter(reference=reference)    
            if not object_with_similar_reference:
                self.reference = reference
        super().save(*args, **kwargs)
    
    def amount_value(self):
        return self.amount*100