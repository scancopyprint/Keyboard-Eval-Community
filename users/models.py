from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

# ———— 管理员模型 ————
class AdminManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, contact, **extra_fields):
        if not username:
            raise ValueError("管理员名称必须填写")
        admin = self.model(username=username, contact=contact, **extra_fields)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_user(self, username, password=None, contact=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, contact, **extra_fields)

    def create_superuser(self, username, password, contact=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, contact, **extra_fields)


class Admin(AbstractBaseUser, PermissionsMixin):
    id       = models.AutoField(primary_key=True, verbose_name="管理员ID")
    username = models.CharField(_("管理员名称"), max_length=50, unique=True)
    contact  = models.CharField(_("联系方式"),   max_length=20)
    # AbstractBaseUser 已包含 password 字段
    is_active = models.BooleanField(_("活跃"), default=True)
    is_staff  = models.BooleanField(_("可登录后台"), default=True)

    objects = AdminManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['contact']

    class Meta:
        db_table = 'users_admin'
        verbose_name = _("管理员")
        verbose_name_plural = _("管理员列表")

    def __str__(self):
        return self.username


# ———— 评价者模型 ————
class Evaluator(models.Model):
    id                = models.AutoField(primary_key=True, verbose_name="评价者ID")
    username          = models.CharField(_("评价者名称"), max_length=50, unique=True)
    password          = models.CharField(_("密码"),      max_length=128)
    bio               = models.TextField(_("简介"),    blank=True)
    registration_date = models.DateTimeField(_("注册日期"), auto_now_add=True)

    class Meta:
        db_table = 'users_evaluator'
        verbose_name = _("评价者")
        verbose_name_plural = _("评价者列表")

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)
        self.save(update_fields=['password'])

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)
