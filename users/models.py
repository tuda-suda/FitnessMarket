from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDERS = (
        ("M", "Мужчина"),
        ("F", "Женщина"),
    )


class Client(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
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
    user = models.OneToOneField(User, models.CASCADE)
    clients = models.ForeignKey(Client, models.CASCADE, "clients")
    sport = models.CharField('вид спорта', max_length=50)
    cost = models.PositiveSmallIntegerField('рублей за час')


@receiver(post_save, sender=User)
def create_user_profile(sender, model, instance, created, **kwargs):
    if created:
        if model == Client:
            Client.objects.create(user=instance)
        else:
            Trainer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, model, instance, **kwargs):
    if model == Client:
        instance.client.save()
    else:
        instance.trainer.save()


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


class TrainingProgramm(models.Model):
    client = models.ForeignKey(Client, models.CASCADE, "program")
    trainer = models.ForeignKey(Trainer, models.CASCADE, "programs")
    text = models.TextField('программа тренировок')
    
    class Meta:
        unique_together = [ "client", "trainer"]
