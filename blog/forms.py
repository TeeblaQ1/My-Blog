from django import forms
from .models import Comment, ContactUs

class EmailPostForm(forms.Form):
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	comment = forms.CharField(required=False, widget=forms.Textarea)
	
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('name', 'email', 'body')
class SearchForm(forms.Form):
	query = forms.CharField()

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		fields = '__all__'
		widgets = {
				'name': forms.TextInput(attrs={'placeholder': 'Name'}),
				'email': forms.TextInput(attrs={'placeholder': 'Email Address'}),
				'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
				'message': forms.Textarea(attrs={'placeholder': 'Message'})
		}