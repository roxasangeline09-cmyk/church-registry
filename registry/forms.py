import re
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Member, Sacrament, BaptismDetail, ConfirmationDetail, CommunionDetail, MarriageDetail, LastRitesDetail, Pledge, PledgePayment


def validate_letters_only(value, field_name='This field'):
    if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s\-'.]+$", value):
        raise ValidationError(f'{field_name} must contain letters only.')


def validate_ph_contact(value):
    cleaned = re.sub(r'\s+', '', value)
    if not re.match(r'^09\d{9}$', cleaned):
        raise ValidationError('Enter a valid 11-digit Philippine mobile number starting with 09.')


def validate_not_future(value):
    if value > date.today():
        raise ValidationError('Date cannot be in the future.')


def validate_positive_amount(value):
    if value <= 0:
        raise ValidationError('Amount must be greater than zero.')


class MemberForm(forms.ModelForm):
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = Member
        fields = ['first_name', 'middle_name', 'last_name', 'suffix', 'birthdate',
                  'gender', 'civil_status', 'address', 'contact_number', 'email']
        widgets = {
            'first_name':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Juan'}),
            'middle_name':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'last_name':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Dela Cruz'}),
            'suffix':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Jr., Sr., III'}),
            'gender':         forms.Select(attrs={'class': 'form-select'}),
            'civil_status':   forms.Select(attrs={'class': 'form-select'}),
            'address':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09XXXXXXXXX', 'maxlength': '11'}),
            'email':          forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
        }

    def clean_first_name(self):
        value = self.cleaned_data['first_name'].strip()
        validate_letters_only(value, 'First name')
        return value.title()

    def clean_middle_name(self):
        value = (self.cleaned_data.get('middle_name') or '').strip()
        if value:
            validate_letters_only(value, 'Middle name')
            return value.title()
        return value

    def clean_last_name(self):
        value = self.cleaned_data['last_name'].strip()
        validate_letters_only(value, 'Last name')
        return value.title()

    def clean_birthdate(self):
        value = self.cleaned_data.get('birthdate')
        if value:
            if value > date.today():
                raise ValidationError('Birthdate cannot be in the future.')
            if value.year < 1900:
                raise ValidationError('Please enter a valid birthdate.')
        return value

    def clean_contact_number(self):
        value = (self.cleaned_data.get('contact_number') or '').strip()
        if value:
            validate_ph_contact(value)
        return value

    def clean_email(self):
        value = (self.cleaned_data.get('email') or '').strip()
        if value:
            qs = Member.objects.filter(email=value)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('A member with this email already exists.')
        return value


class SacramentForm(forms.ModelForm):
    date_received = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Sacrament
        fields = ['date_received', 'officiant_name', 'place', 'remarks']
        widgets = {
            'officiant_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fr. / Bishop Full Name'}),
            'place':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church / Location'}),
            'remarks':        forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_date_received(self):
        value = self.cleaned_data['date_received']
        validate_not_future(value)
        return value


class BaptismDetailForm(forms.ModelForm):
    class Meta:
        model = BaptismDetail
        fields = ['father_name', 'mother_name']
        widgets = {
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's full name"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mother's full name"}),
        }


class ConfirmationDetailForm(forms.ModelForm):
    class Meta:
        model = ConfirmationDetail
        fields = ['confirmation_name']
        widgets = {
            'confirmation_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Maria'}),
        }


class CommunionDetailForm(forms.ModelForm):
    class Meta:
        model = CommunionDetail
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MarriageDetailForm(forms.ModelForm):
    class Meta:
        model = MarriageDetail
        fields = ['spouse_name']
        widgets = {
            'spouse_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name of spouse'}),
        }


class LastRitesDetailForm(forms.ModelForm):
    class Meta:
        model = LastRitesDetail
        fields = ['condition_notes', 'family_contact']
        widgets = {
            'condition_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'family_contact':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person / number'}),
        }


class PledgeForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    )

    class Meta:
        model = Pledge
        fields = ['member', 'description', 'amount_pledged', 'due_date']
        widgets = {
            'member':        forms.Select(attrs={'class': 'form-select'}),
            'description':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Church Renovation Fund'}),
            'amount_pledged': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': '0.00'}),
        }

    def clean_amount_pledged(self):
        value = self.cleaned_data['amount_pledged']
        validate_positive_amount(value)
        return value


class PledgePaymentForm(forms.ModelForm):
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = PledgePayment
        fields = ['amount_paid', 'payment_date', 'payment_method', 'remarks']
        widgets = {
            'amount_paid':    forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1', 'placeholder': '0.00'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Cash, GCash'}),
            'remarks':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional notes'}),
        }

    def clean_amount_paid(self):
        value = self.cleaned_data['amount_paid']
        validate_positive_amount(value)
        return value

    def clean_payment_date(self):
        value = self.cleaned_data['payment_date']
        validate_not_future(value)
        return value
