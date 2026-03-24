from django import forms
from .models import Member, Baptism, Confirmation, FirstHolyCommunion, Marriage, LastRites, Pledge, PledgePayment


class MemberForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Member
        exclude = ['is_active', 'date_registered']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'civil_status': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class BaptismForm(forms.ModelForm):
    date_baptized = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Baptism
        exclude = ['member']
        widgets = {
            'priest': forms.TextInput(attrs={'class': 'form-control'}),
            'godfather': forms.TextInput(attrs={'class': 'form-control'}),
            'godmother': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_certificate_no': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ConfirmationForm(forms.ModelForm):
    date_confirmed = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Confirmation
        exclude = ['member']
        widgets = {
            'bishop': forms.TextInput(attrs={'class': 'form-control'}),
            'confirmation_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sponsor': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CommunionForm(forms.ModelForm):
    date_received = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = FirstHolyCommunion
        exclude = ['member']
        widgets = {
            'priest': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MarriageForm(forms.ModelForm):
    date_married = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Marriage
        exclude = ['member']
        widgets = {
            'spouse_name': forms.TextInput(attrs={'class': 'form-control'}),
            'priest': forms.TextInput(attrs={'class': 'form-control'}),
            'principal_sponsor': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_sponsor': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LastRitesForm(forms.ModelForm):
    date_administered = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = LastRites
        exclude = ['member']
        widgets = {
            'priest': forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PledgeForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Pledge
        exclude = ['status', 'date_created']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_pledged': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class PledgePaymentForm(forms.ModelForm):
    date_paid = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = PledgePayment
        exclude = ['pledge']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }
