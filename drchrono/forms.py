from django import forms

# forms go here
class birthdayEmailForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, max_length=1000)


class CheckinForm(forms.Form):
    fname = forms.CharField(max_length=20, label='First Name' ,widget=forms.TextInput(attrs={'required': True}))
    lname = forms.CharField(max_length=20, label='Last Name', widget=forms.TextInput(attrs={'required': True}))
    ssn = forms.RegexField(
        label= 'Social Security Number(SSN)',
        regex= '^(\d{3}\-\d{2}\-\d{4})$',
        widget= forms.TextInput(attrs={'required': True})
    )

class DemographicsForm(forms.Form):
    fname = forms.CharField(max_length=20, label='First Name' ,widget=forms.TextInput(attrs={'required': True}))
    lname = forms.CharField(max_length=20, label='Last Name', widget=forms.TextInput(attrs={'required': True}))
    ssn = forms.RegexField(
        label= 'Social Security Number(SSN)',
        regex= '^(\d{3}\-\d{2}\-\d{4})$',
        widget= forms.TextInput(attrs={'required': True})
    )

