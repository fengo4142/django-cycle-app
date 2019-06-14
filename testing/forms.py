from django import forms
from django.forms.formsets import formset_factory
from django.forms import BaseFormSet
from .models import  sampling
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SamplingForm(forms.Form):
	# Population_Size = forms.IntegerField(required=False)
	
	def __init__(self, *args, **kwargs):
		# self.control_procedures = kwargs.pop('control_procedures', [])
		# kwargs['auto_id'] = "%s".format(self.control_procedures)
		# print(kwargs)
		super(SamplingForm, self).__init__(*args, **kwargs)
		# self.fields['Population_Size'] = forms.IntegerField()
		# self.fields['Population_Size'].required = False
		self.fields['Estimated_Population_Exception_Rate'] = forms.IntegerField()
		self.fields['Estimated_Population_Exception_Rate'].required = False
		self.fields['Tolerable_Exception_Rate'] = forms.IntegerField()
		self.fields['Tolerable_Exception_Rate'].required = False
		self.fields['Suggested_Sample_Size'] = forms.IntegerField()
		self.fields['Suggested_Sample_Size'].required = False
		self.fields['Actual_Sample_Size'] = forms.IntegerField()
		self.fields['Actual_Sample_Size'].required = False
		self.fields['Population_Size'] = forms.IntegerField(required=False)
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-lg-5 mb-1'
		self.helper.field_class = 'form-group col-md-3 mb-0'
		
            
		# self.fields['Number_of_Exceptions'].required = False
		# self.fields['Sample_Exception_Rate'].required = False
		# self.fields['Computed_Upper_Exception_Rate'].required = False

	




# class BaseSamplingFormset(BaseFormSet):

# 	def __init__(self, *args, **kwargs):
# 		self.control_proceduress = kwargs.pop('control_proceduress', [])
# 		# print(self.control_proceduress)
# 		self.extra = len(self.control_proceduress)
# 		self.max_num = len(self.control_proceduress)
# 		# print(self.max_num)
# 		self.absolute_max = len(self.control_proceduress)
# 		# print(self.absolute_max)
# 		self.validate_max = len(self.control_proceduress)
# 		# print(self.validate_max)
# 		super(BaseSamplingFormset, self).__init__(*args, **kwargs)

# 	def _construct_form(self, i, **kwargs):
# 		kwargs['control_procedures'] = self.control_proceduress[i]
# 		# print(kwargs['control_procedures'])
# 		form = super(BaseSamplingFormset, self)._construct_form(i, **kwargs)
# 		# print(form)
# 		return form



# BaseSamplingDatasheetFormset= formset_factory(form=SamplingForm, formset=BaseSamplingFormset)
# print(BaseFormSet)


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user