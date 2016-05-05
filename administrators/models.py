from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.utils import timezone
from django.core import validators
from django.utils.translation import ugettext_lazy as _
import re
import datetime
from django.core.cache import cache
from django.core.mail import send_mail


# Create your models here.
class CUserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active = True
        user.save(using=self._db)
        return user


class CUser(AbstractBaseUser):
    username = models.CharField('username', max_length=30, unique=True,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
                                validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'), 'Enter a valid username.', 'invalid')])
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'), max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    receive_newsletter = models.BooleanField(_('receive newsletter'), default=False)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True,
                                    help_text=_('The groups this user belongs to. A user will get all permissions granted to each of his/her group.'),
                                    related_name="tmp_user_set", related_query_name="user")
    user_permissions = models.ManyToManyField(Permission,
                                              verbose_name=_('user permissions'), blank=True,
                                              help_text=_('Specific permissions for this user.'),
                                              related_name="tmp_user_set", related_query_name="user")
    objects = CUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def last_seen(self):
        return cache.get('seen_%s' % self.username)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # def online(self):
    #     if self.last_seen():
    #         now = datetime.datetime.now()
    #         if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
    #             return False
    #         else:
    #             return True
    #     else:
    #         return False