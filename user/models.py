# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import hashlib


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         user = self.model(email=self.normalize_email(
#             email),  **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email,  password):
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True, primary_key=True)
#     first_name = models.CharField(_('First Name'), max_length=30, blank=True)
#     last_name = models.CharField(_('Last Name'), max_length=150, blank=True)
#     is_active = models.BooleanField(_('Is Active'), default=True)
#     is_staff = models.BooleanField(_('Is Staff'), default=False)
#     is_suspended = models.BooleanField(_('Is Suspend'), default=False)
#     isEmailVerified = models.BooleanField(_('Is Email Verified'), default=False)
#     isPhoneVerified = models.BooleanField(_('Is Phone Verified'), default=False)
#     smsProvider = models.BooleanField(_('User Sms Provider'), default=False)
#
#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#
#     phoneNumber = models.CharField(_('User Phone Number'), blank=True, unique=True, null=True, max_length=25)
#
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=_('User Groups'),
#         blank=True,
#         help_text=_(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#         related_name="users",
#         related_query_name="user",
#     )
#
#     class Meta:
#         verbose_name = _('User')
#         verbose_name_plural = _('Users')
#
#     def __str__(self):
#         return self.first_name + " " + self.last_name


# class AuthToken(models.Model):
#     user = models.ForeignKey('auth.User', verbose_name=_('Model LoginToken Field user'), related_name='tokens', on_delete=models.CASCADE)
#     token = models.CharField(verbose_name=_('Model LoginToken Field token'), max_length=200)
#     create_date = models.DateTimeField(verbose_name=_('Model LoginToken Field create_date'), null=False, blank=True, editable=False)
#     expire_date = models.DateTimeField(verbose_name=_('Model LoginToken Field expire_date'), null=False, blank=True, editable=False)
#
#     def save(self, *args, **kwargs):
#         if self.create_date is None:
#             self.create_date = timezone.now()
#
#             random_string = "mflsnefalja" + str(self.create_date)
#             user_unique_string= (self.user.email + random_string).encode("utf-8")
#             self.token = hashlib.md5(user_unique_string).hexdigest()
#
#         return super(AuthToken, self).save(*args, **kwargs)
