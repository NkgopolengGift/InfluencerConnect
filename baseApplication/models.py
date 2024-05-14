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
    account_type = models.CharField(max_length=50)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # New field added here
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    objects = UserTBLManager()

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

#################-SPONSORSTBL-###################
