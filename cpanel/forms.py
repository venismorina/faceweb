from django import forms
from sendreq.models import myUser

class TimeInput(forms.TimeInput):
    input_type = "time"

class UpdateForm(forms.ModelForm):
    class Meta:
        model = myUser
        fields = ('name', 'place', 'work_hours')

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['work_hours'].widget = TimeInput(attrs={'class':'without',"step":"1"})

