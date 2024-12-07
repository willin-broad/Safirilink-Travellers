from django import forms
from .models import Member
from .models import BusesAvailable


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'fname', 'lname', 'email', 'password', 'amount_paid','seatNumber','vehicle']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BookingForm(forms.ModelForm):
    class Meta:
        model = BusesAvailable
        fields = [
            'BusName',
            'From',
            'BusDestination',
            'NuberOfSeats'
        ]

        widgets = {
            'BusName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bus Name'}),
            'From': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Starting Location'}),
            'BusDestination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Destination'}),
            'NuberOfSeats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Number of Seats'}),
        }


