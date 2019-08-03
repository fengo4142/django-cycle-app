from django import forms
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory
from .models import  sampling, Test_of_Controls, Mxcell, testing_of_controls, Objectives, Cycle_in_obj
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class ObjectivesForm(forms.ModelForm):

	class Meta:
		model = Objectives
		exclude = ('assessed_cr', )
	def __init__(self, *args, **kwargs):
		super(ObjectivesForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		self.fields['transaction_objective'].widget.attrs['style'] = "width:850px"
		#self.fields['transaction_objective'].required = False
		#for i in range(2):
		# 	self.fields['assessed_cr_%d' % i] = forms.ChoiceField(choices = Med_High_CHOICES, required=False)
		#self.fields['cycle'].required = False
		#self.fields['assessed_cr'].required = False

def __str__(self):
		return self.transaction_objective

objective_query = Objectives.objects.all()
ObjectivesFormSet = inlineformset_factory(Cycle_in_obj, Objectives, form=ObjectivesForm, extra=1, can_delete=True, )

class CycleInObjForm(forms.ModelForm):
	class Meta:
		model = Cycle_in_obj
		exclude = ()
	def __init__(self, *args, **kwargs):
		super(CycleInObjForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor


class SamplingForm(forms.Form):
	# Population_Size = forms.IntegerField(required=False)
	
	def __init__(self, *args, **kwargs):
		# self.control_procedures = kwargs.pop('control_procedures', [])
		# kwargs['auto_id'] = "%s".format(self.control_procedures)
		# print(kwargs)
		super(SamplingForm, self).__init__(*args, **kwargs)

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


from django import forms
from cycle.models import Cycle, Cycle_in_obj, Client, Objectives

from django.contrib.auth.forms import UserCreationForm
from django.forms.formsets import formset_factory
from django.forms import BaseFormSet, BaseInlineFormSet
from django.forms.models import inlineformset_factory


class AuditorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_auditor = True
        if commit:
            user.save()
        return user


# class MemberForm(forms.ModelForm):
# 	class Meta:
# 		model = Member
# 		fields = [
# 			"data",
# 			"user"
		
# 		]

class Client_Create_form(forms.ModelForm):
	class Meta:
		model = Client
		exclude = ()


class ICMatrix(forms.Form):
	Tr = 'True'
	Fa = 'False'
	# medium = 'Med'
	# low = 'Low'
	# high = 'High'

	# Med_High_CHOICES = (
	# 	(medium, 'Med'),
	# 	(low, 'Low'),
	# 	(high, 'High'),
	# 	)
		

	Yes_No_CHOICES = (
    (Tr, 'True'),
    (Fa, 'False'),
)
	
	# option = forms.ChoiceField(choices = Yes_No_CHOICES)
	# assessed_cr = forms.ChoiceField(choices = Med_High_CHOICES)
	objectives = Objectives.objects.all().values_list('transaction_objective', flat=True)

	def __init__(self, *args, **kwargs):
		Tr = 'True'
		Fa = 'False'
		
		Yes_No_CHOICES = (
			(Tr, 'True'),
			(Fa, 'False'),
			)

		# print(kwargs)
		self.mxcell = kwargs.pop('mxcell', [])
		kwargs['auto_id'] = "%s".format(self.mxcell)
		super(ICMatrix, self).__init__(*args, **kwargs)
		for i in range(2):
			self.fields['option_%d' % i] = forms.ChoiceField(choices = Yes_No_CHOICES)
		# for i in range(4):
		# 	self.fields['assessed_cr_%d' % i] = forms.ChoiceField(choices = Med_High_CHOICES)


class BaseICMatrixFormset(BaseFormSet):
	def __init__(self, *args, **kwargs):
		# print(kwargs)
		self.mxcells = kwargs.pop('mxcells', [])

		# print(self.objectives)
		# self.objectives = kwargs.pop('objectives', [])
		# print(self.objectives)
		self.extra = len(self.mxcells)
		self.max_num = len(self.mxcells)
		self.absolute_max = len(self.mxcells)
		self.validate_max = len(self.mxcells)
		super(BaseICMatrixFormset, self).__init__(*args, **kwargs)


	def _construct_form(self, i, **kwargs):
		kwargs['mxcell'] = self.mxcells[i]
		
		# print(kwargs)
		form = super(BaseICMatrixFormset, self)._construct_form(i, **kwargs)
		# print(form)
		return form

BaseFormset= formset_factory(form=ICMatrix, formset=BaseICMatrixFormset)
print(BaseFormSet)

class ObjectivesForm(forms.ModelForm):
	
	class Meta:
		model = Objectives
		exclude = ('assessed_cr',)

	def __init__(self, *args, **kwargs):
		super(ObjectivesForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		self.fields['transaction_objective'].widget.attrs['style'] = "width:850px"
		# self.fields['transaction_objective'].required = False
		# for i in range(2):
		# 	self.fields['assessed_cr_%d' % i] = forms.ChoiceField(choices = Med_High_CHOICES, required=False)
		# self.fields['cycle'].required = False
		# self.fields['assessed_cr'].required = False

objective_query = Objectives.objects.all()
ObjectivesFormSet = inlineformset_factory(Cycle_in_obj, Objectives, form=ObjectivesForm,
	extra=1, can_delete=True, )


class NewCycleForm(forms.ModelForm):
	
	class Meta:
		model = Cycle
		exclude = ()

	def __init__(self, *args, **kwargs):
		super(NewCycleForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		self.fields['cycle_type'].widget.attrs['style'] = "width:850px"	

#NewCycleFormSet = inlineformset_factory(Client_Create, Cycle,  form=NewCycleForm, extra=1, can_delete=True, )

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit

#from .custom_layout_object import *


class CycleForm(forms.ModelForm):

    class Meta:
        model = Cycle
        exclude = ()

    # def __init__(self, *args, **kwargs):
    #     super(CycleForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_tag = True
    #     self.helper.form_class = 'form-horizontal'
    #     self.helper.label_class = 'col-md-4 create-label'
    #     self.helper.field_class = 'col-md-9'
    #     # self.helper.fields["transaction_objective"].queryset = Objectives.objects.all()
    #     # self.helper.template = 'bootstrap/table_inline_formset.html'
    #     self.helper.layout = Layout(
    #         Div(
    #             Field('cycle_name'),
    #             Fieldset('Transaction Objectives',
    #                 Formset('titles')),

    #             # Field('note'),
    #             HTML("<br>"),
    #             ButtonHolder(Submit('submit', 'save')),
    #             )
    #         )




class ICProcedures(forms.ModelForm):
	
	class Meta:
		model = Mxcell
		exclude = ()
	# value = Mxcell.objects.all()	

	def __init__(self, *args, **kwargs):
		super(ICProcedures, self).__init__(*args, **kwargs)
		self.fields['objectives'].required = False
		self.fields['style'].required = False
		self.fields['value'].required = False
		self.helper = FormHelper()
		self.helper.form_tag = True
		self.helper.form_class = 'form-row'
		self.helper.label_class = 'form-group col-md-6 mb-0'
		self.helper.field_class = 'form-group col-md-6 mb-0'
		self.helper.layout = Layout(

                Fieldset('Procedures against Control Activity',
                    Formset('titles')),
                    
                # Field('note'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            


class TOCForm(forms.ModelForm):
	
	class Meta:
		model = Test_of_Controls
		exclude = ()

	def __init__(self, *args, **kwargs):
		super(TOCForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
		self.fields['control_procedures'] = forms.CharField(max_length=150)
		self.fields['control_procedures'].widget.attrs['style'] = "width:650px"
		self.fields['control_procedures'].label = "Internal Control Procedures"
		self.fields['control_procedures'].widget.attrs['placeholder'] = 'Control Procedures'
		self.fields['value'] = forms.ModelChoiceField(queryset =Mxcell.objects.all())
		self.fields['value'].label = "Internal Control Activity"

		# self.fields['mxcell'] = forms.CharField(max_length=150)
		# self.fields['mxcell'].queryset = Test_of_Controls.objects.all().values('mxcell')
		      		
BaseICProcFormset= inlineformset_factory(Mxcell, Test_of_Controls, form=TOCForm, extra=1, can_delete=True)

# class SamplingForm(forms.ModelForm):

# 	class Meta:
# 		model = sampling
# 		fields = ['control_procedures','Estimated_Population_Exception_Rate', 'Tolerable_Exception_Rate', 
# 					'Sample_Size', 'Population_Size']
	
# 	def __init__(self, *args, **kwargs):
# 		self.control_procedures = kwargs.pop('control_procedures', [])
# 		kwargs['auto_id'] = "%s".format(self.control_procedures)
# 		print(kwargs)
# 		super(SamplingForm, self).__init__(*args, **kwargs)



# class BaseSamplingFormset(BaseFormset):

# 	def __init__(self, *args, **kwargs):
# 		self.control_proceduress = kwargs.pop('control_proceduress', [])
# 		# print(self.control_proceduress)
# 		self.extra = len(self.control_proceduress)
# 		self.max_num = len(self.control_proceduress)
# 		self.absolute_max = len(self.control_proceduress)
# 		self.validate_max = len(self.control_proceduress)
# 		super(BaseSamplingFormset, self).__init__(*args, **kwargs)

# 	def _construct_form(self, i, **kwargs):
# 		kwargs['control_procedures'] = self.control_proceduress[i]
# 		print(kwargs['control_procedures'])
# 		form = super(BaseSamplingFormset, self)._construct_form(i, **kwargs)
# 		print(form)
# 		return form



# BaseSamplingDatasheetFormset= formset_factory(form=SamplingForm, formset=BaseSamplingFormset)
# # print(BaseFormSet)

class samples_form(forms.Form):

	
	Random = 'Random'
	Condition = 'Condition'
	Weights = 'Weights'


	Sampling_CHOICES = (
		(Random, 'Random'),
	)

	sampling_method = forms.ChoiceField(choices = Sampling_CHOICES, initial={'sampling_method': 'Random'}, required = False)
	sampling_size = forms.IntegerField(required = False)
	#field_selected = forms.CharField(max_length=20, required=False)
	#field_selected_value = forms.IntegerField(required=False)
	# Population = forms.FileField()
	


	def __init__(self, data=None, *args, **kwargs):

		super(samples_form, self).__init__(data, *args, **kwargs)


		#if data and data.get('sampling_method', None) == self.Condition:
		#	self.fields['field_selected'].required = True
		#	self.fields['field_selected_value'].required = True

class TOC_Form(forms.ModelForm):
		Option_CHOICES = [
				['deficient', 'deficient'],['indeficient','indeficient'],
		]
		class Meta:
			model = testing_of_controls
			fields = [
				"remarks",
				"attachment",
				"deficient",
			]

		def __init__(self, *args, **kwargs):
			super(TOC_Form, self).__init__(*args, **kwargs)
			self.fields['remarks'].widget.attrs['rows'] = 4
			self.fields['remarks'].required = False
			self.fields['deficient'] = forms.ChoiceField(label="Deficient or Not?", widget=forms.RadioSelect(), choices=self.Option_CHOICES)	
			self.fields['deficient'].required = False
			self.fields['attachment'] = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),)
			self.fields['attachment'].required = False
			self.helper = FormHelper()
			self.helper.form_tag = True
			self.helper.form_class = 'form-horizontal'
			self.helper.label_class = 'col-lg-2 mb-3'
			self.helper.field_class = 'form-group col-md-6 mb-0'
			self.helper.layout = Layout(
                Fieldset('Procedures against Control Activity', Fieldset('titles')),
                #Field('note'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
			)
		
class MyForm(forms.Form):
    original_field = forms.CharField()
    extra_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = \
                forms.CharField()
	
	

class TransactionObjectivesForm(forms.ModelForm):
	
	class Meta:
		model = Objectives
		exclude = ('assessed_cr','user',)

	def __init__(self, *args, **kwargs):
		super(TransactionObjectivesForm, self).__init__(*args, **kwargs)
		self.fields['cycle'].widget.attrs['style'] = "width:280px; height:28px;"
		self.fields['cycle'].required = False



	# 	self.user = kwargs.pop('user', None)
	# # 	extra_fields = kwargs.pop('extra', 6)
	# 	super(TransactionObjectivesForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
	# 	# self.fields['transaction_objective'].widget.attrs['style'] = "width:850px"
	# 	# self.fields['transaction_objective'].required = False
	# 	self.fields['extra_field_count'] = forms.CharField(widget=forms.HiddenInput())
	# 	self.fields['extra_field_count'].initial = extra_fields

	# 	for index in range(int(extra_fields)):
	# 		self.fields['Transaction_Objective_{index}'.format(index=index)] = \
 #        		forms.CharField()
	# 		self.fields['Transaction_Objective_{index}'.format(index=index)].widget.attrs['style'] = "width:850px"

# CompoundFormset = formset_factory(TransactionObjectivesForm,max_num=10,extra=1)

class CompoundFormset(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        transaction_objective = []
        duplicates = False

        for form in self.forms:
            i = self.total_form_count()
            print(i)
          



