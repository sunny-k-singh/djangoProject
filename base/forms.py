from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__' #this two lines will create a form based on meta data of Room table
        exclude=['participants','host']
        