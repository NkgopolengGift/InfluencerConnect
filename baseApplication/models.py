from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

#################-USERSTBL-###################

class UserTBLManager(BaseUserManager):
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

class UserTBL(AbstractBaseUser):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(max_length=70)
    phone_number = models.CharField(max_length=30)
    account_type = models.CharField(max_length=15)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # New field added here
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserTBLManager()

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
    user_id = models.ForeignKey(UserTBL, on_delete=models.CASCADE)
    #username = models.CharField(max_length=100, unique=True)
    content_category = models.CharField(max_length=100)

    def __str__(self):
        return self.username

#################-SPONSORTBL-###################

class Sponsor(models.Model):
    sponser_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserTBL, on_delete=models.CASCADE)
    content_category = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

#################-PLATFORMTBL-###################

class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    influencer_id = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=100)
    platform_url = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.platform_name
    
#################-Chat-###################
class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    influencer_id = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    sponser_id = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    message_content = models.CharField(max_length=245, null=False)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

#################-Payment-###################

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    influencer_id = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    sponser_id = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    card_details = models.CharField(max_length=150, null=False)
    amount = models.CharField(max_length=8, null=False)
    billing_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.id.username
