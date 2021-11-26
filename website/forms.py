from django import forms
from .models import Image,UserDetails,UpdateProfileImage,Comment
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth.models import User

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user



class CustomAuthenticationForm(AuthenticationForm):
	class Meta:
		fields=("username","password")

    



class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields=("content","title","file","user") 



class UserDetailsForm(forms.ModelForm):
	class Meta:
		model=UserDetails
		fields="__all__"


class UpdateProfileImageForm(forms.ModelForm):
	class Meta:
		model=UpdateProfileImage
		fields="__all__"

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=("id","user","image","comment")

class PasswordChangeForm(PasswordChangeForm):
	class Meta:
		model=User
		fields="__all__"