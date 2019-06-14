from django import forms
from cycle.models import Objectives, Cycle_in_obj
from django.forms import inlineformset_factory

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