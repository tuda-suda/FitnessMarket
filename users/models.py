from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDERS = (
        ("M", "Мужчина"),
        ("F", "Женщина"),
    )

REGIONS = (
    ("1", "Москва"),
    ("2", "Казань"),
    ("3", "Владивосток"),
    ("4", "Калининград")
)

class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)


class Client(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='client')
    user.is_client = True
    goal = models.TextField('цель тренировок')
    diseases = models.TextField('противопоказания', blank=True, null=True)
    date_joined = models.DateTimeField(
        'дата регистрации', 
        auto_now_add=True
    )
    gender = models.CharField('пол', max_length=1, choices=GENDERS)
    height = models.PositiveSmallIntegerField('рост', blank=True)
    weight = models.PositiveSmallIntegerField('вес', blank=True)
    birth_date = models.DateField('дата рождения', null=True, blank=True)


class Trainer(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name='trainer')
    user.is_trainer = True
    location = models.CharField(max_length=100, choices=REGIONS)
    gender = models.CharField('пол', max_length=1, choices=GENDERS)
    clients = models.ForeignKey(Client, models.CASCADE, "clients")
    sport = models.CharField('вид спорта', max_length=50, blank=True, null=True)
    cost = models.PositiveSmallIntegerField('рублей за час', blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_trainer:
            Trainer.objects.create(user=instance)
        elif instance.is_client:
            Client.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_trainer:
        instance.trainer.save()
    elif instance.is_client:
        instance.client.save()


class Review(models.Model):
    MARKS = (
        ('1', 'Неквалифицированный тренер'),
        ('2', 'Плохой тренер'),
        ('3', 'Нормальный тренер'),
        ('4', 'Хороший тренер'),
        ('5', 'Лучший тренер')
    )
    author = models.ForeignKey(Client, models.CASCADE, "client_reviews")
    trainer = models.ForeignKey(Client, models.CASCADE, "trainer_reviews")
    text = models.TextField('отзыв')
    created = models.DateTimeField('дата публикации', auto_now_add=True)
    rate = models.CharField('оценка', max_length=1, choices=MARKS)


class TrainingProgram(models.Model):
    client = models.ForeignKey(Client, models.CASCADE, "program")
    trainer = models.ForeignKey(Trainer, models.CASCADE, "programs")
    text = models.TextField('программа тренировок')
    
    class Meta:
        unique_together = [ "client", "trainer"]
