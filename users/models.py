from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDERS = (
        ("M", "Мужчина"),
        ("F", "Женщина"),
    )

class Customer(models.Model):
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


class Instructor(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, "customers")
    user = models.OneToOneField(User, models.CASCADE)
    sport = models.CharField('вид спорта', max_length=50)
    cost = models.PositiveSmallIntegerField('рублей за час')



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, model="Customer", **kwargs):
    if created:
        if model == "Customer":
            Customer.objects.create(user=instance)
        else:
            Instructor.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, model, **kwargs):
    if model == "Customer":
        instance.customer.save()
    else:
        instance.instructor.save()


class Feedback(models.Model):
    MARKS = (
        (1, 'Неквалифицированный тренер'),
        (2, 'Плохой тренер'),
        (3, 'Нормальный тренер'),
        (4, 'Хороший тренер'),
        (5, 'Лучшей тренер')
    )
    author = models.ForeignKey(Customer, models.CASCADE, "feedbacks")
    instructor = models.ForeignKey(Customer, models.CASCADE, "feedbacks")
    text = models.TextField('отзыв')
    created = models.DateTimeField('дата публикации', auto_now_add=True)
    rate = models.PositiveSmallIntegerField('оценка', max_length=1, choices=MARKS)


class Programm(models.Model):
    customer = models.ForeignKey(Customer, models.CASCADE, "programm")
    instructor = models.ForeignKey(Customer, models.CASCADE, "programms")
    text = models.TextField('программа тренировок')
    
    class Meta:
        unique_together = ["customer", "instructor"]
