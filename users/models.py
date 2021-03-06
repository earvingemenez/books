from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """ user manager
    """
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        instance = self.model(email=email, username=email)
        instance.set_password(password)
        instance.save()

        return instance

    def create_superuser(self, email, password, **kwargs):
        instance = self.create_user(email, password, **kwargs)
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()

        return instance


class User(AbstractBaseUser, PermissionsMixin):
    """ user model
    """
    email = models.EmailField(max_length=150, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    job_title = models.CharField(max_length=150, null=True, blank=True)
    quote = models.CharField(max_length=250, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    country = models.CharField(max_length=150, null=True, blank=True)

    image = models.ImageField(upload_to="users/", null=True, blank=True)

    fans = models.ManyToManyField('self', blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return "{email}".format(email=self.email)

    def get_full_name(self):
        """ Returns the first_name pluse the last_name, with a space
            in between.
        """
        return "{first} {last}".format(
            first=self.first_name,
            last=self.last_name,
        ).strip()

    def get_short_name(self):
        """ Returns the short name for the user.
        """
        return "{}".format(self.first_name)

    def follow(self, fan):
        if self.fans.filter(id=fan.id).exists():
            self.fans.remove(fan)
            return
        
        self.fans.add(fan)
        return


class Commendation(models.Model):
    """ user commendation
    """
    author = models.ForeignKey(User)
    content = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}| {}".format(self.author, self.date_created)