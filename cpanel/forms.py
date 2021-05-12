from django import forms
from sendreq.models import myUser
from django.contrib.auth.models import User

class TimeInput(forms.TimeInput):
    input_type = "time"

class UpdateForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ('name', 'place', 'work_hours')

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['work_hours'].widget = TimeInput(attrs={'class':'without',"step":"1"})
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'



