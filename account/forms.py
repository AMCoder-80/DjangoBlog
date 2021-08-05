# Inherit from django forms
from django import forms
from .models import User

# For model forms we should inherit like this
class ProfileForm(forms.ModelForm):

    # Overwriting the init method to let ourself to modify some behavior of form fields
    # By overwriting we tell python to permit us to access the base class attributes
    def __init__(self, *args, user, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # This will disable the help text
        self.fields['username'].help_text = None

        # Here we define, if user were not super user, make some fields readonly
        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['is_author'].disabled = True
            self.fields['special_user'].disabled = True

    # Our model and the needed fields should be defined in meta class
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_author', 'special_user']
