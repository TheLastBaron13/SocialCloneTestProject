from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# ne ti treba model radi default classa UserCreationForm
# Meta klasa ti e za da prais customise na atritutite na meta clasata (UserCreationForm)
class UserCreateForm(UserCreationForm):

    class Meta:

        fields = ('username','email','password1','password2')
        model = get_user_model()
# super() fakticki dodava label atrribut na fields atributot na UserCreateForm  da bide Display Name
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label='Display Name'
        self.fields['email'].label = "Email Address"
