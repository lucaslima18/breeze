from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    '''
        this form define the fields
        hat will be required in the user
        creation
    '''
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'age', )


class CustomUserChangeForm(UserChangeForm):
    '''
        this form define the fields
        hat will be required in the user
        update
    '''
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', )