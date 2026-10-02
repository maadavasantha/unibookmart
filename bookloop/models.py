from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES=(('sellbro','SellBro'),('buybro','BuyBro'),
                  )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES)


    def __str__(self):
        return self.user.username
    
class Book(models.Model):
    sellbro = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    subject= models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    condition =models.CharField(max_length=50)
    is_sold = models.BooleanField(default=False)
    posted_data=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='buybro')