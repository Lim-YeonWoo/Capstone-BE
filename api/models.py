from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils.timezone import localdate, localtime

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, id, name, email, password, **extra_fields):
        if not id:
            raise ValueError('Users require an id field')
        if not name:
            raise ValueError('Users require a name field')
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(id=id, name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id, name, email, password=None, **extra_fields):
        return self._create_user(id, name, email, password, **extra_fields)

    def create_superuser(self, id, name, email, password, **extra_fields):
        user = self.create_user(
            id=id,
            name=name,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, BaseModel):
    id = models.CharField(max_length=25, primary_key=True)
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'name', ]

    def __str__(self):
        return self.name


class Group(BaseModel):
    name = models.CharField(max_length=20)


class UserGroup(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)


class Trip(BaseModel):
    group = models.IntegerField()
    place = models.CharField(max_length=50)
    departing_date = models.DateField(default=localdate)
    arriving_date = models.DateField(default=localdate)
    thumbnail = models.TextField(null=True)


class Photo(BaseModel):
    file_key = models.UUIDField(unique=True)
    file_name = models.CharField(blank=True, max_length=255)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    url = models.TextField()
    tag_yolo = models.ManyToManyField('TagYolo', related_name='photos')
    tag_face = models.ManyToManyField('TagFace', related_name='photos')
    taken_at = models.DateTimeField(null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_sorted_yolo = models.BooleanField(default=False)


class TagYolo(models.Model):
    tag_name = models.CharField(max_length=20)


class TagFace(models.Model):
    tag_num = models.IntegerField()
    custom_name = models.CharField(blank=True, max_length=255)


