from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models
from django.utils import timezone
from django.utils.timezone import now


class MemberManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class Member(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, null=True)
    amount_paid = models.CharField(max_length=100,null=True, blank=True)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    seatNumber = models.CharField(max_length=100,null=True, blank=True)
    vehicle = models.CharField(max_length=100,null=True, blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    is_paid =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'username'
    groups = models.ManyToManyField(
        Group,
        verbose_name= ('groups'),
        blank=True,
        help_text= (
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='members'  # Custom related name to avoid clashes
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name= ('user permissions'),
        blank=True,
        help_text= ('Specific permissions for this user.'),
        related_name='members'  # Custom related name to avoid clashes
    )

    def __str__(self):
        return f'{self.username}'

class BusesAvailable(models.Model):
    BusName = models.CharField(max_length=100)
    From = models.CharField(max_length=100, null=True, blank=True)
    BusDestination = models.CharField(max_length=100, null=True, blank=True)
    BusDepartureDate = models.DateTimeField()
    BusArrivalDate = models.DateTimeField()
    Amount = models.CharField(max_length=100, null=True, blank=True)
    NuberOfSeats = models.CharField(max_length=100, null=True, blank=True)


    def time_until_departure(self):
        """
        Calculates the time remaining until the bus departs.
        """
        current_time = now()
        time_diff = self.BusDepartureDate - current_time
        return time_diff if time_diff.total_seconds() > 0 else "Departed"

    def is_booking_enabled(self):
        """
        Checks if booking is still allowed (departure time is in the future).
        """
        return self.BusDepartureDate > timezone.now()

    def __str__(self):
        """
        String representation of the bus.
        """
        return f"{self.BusName} - {self.From} to {self.BusDestination}"
class Notifications(models.Model):
    BusName = models.CharField(max_length=100,null=True, blank=True)
    From = models.CharField(max_length=100, null=True, blank=True)
    BusDestination = models.CharField(max_length=100,null=True,blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    generalNotification = models.CharField(max_length=100, null=True, blank=True)
class MpesaTransaction(models.Model):
    MerchantRequestID = models.CharField(max_length=50)
    CheckoutRequestID = models.CharField(max_length=50)
    ResultCode = models.CharField(max_length=10)
    calculated_amount = models.IntegerField()
    MpesaReceiptNumber = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.MpesaReceiptNumber} - {self.Amount}"
