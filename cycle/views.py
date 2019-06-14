from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db import DatabaseError, transaction
from cycle.models import Cycle_in_obj, Objectives
from cycle.forms import ObjectivesForm, ObjectivesFormSet

class CycleTransactionCreate(CreateView):
	model = Cycle_in_obj
	fields = ['cycle_type', 'client_name']

	template_name = 'cycle_form.html'
	# form_class = CycleForm
	success_url = reverse_lazy('saveData')
	# queryset = Objectives.objects.all()

	def get_context_data(self, **kwargs):
		data = super(CycleTransactionCreate, self).get_context_data(**kwargs)

		if self.request.POST:			
			data['titles'] = ObjectivesFormSet(self.request.POST)
		
		else:
			data['titles'] = ObjectivesFormSet()
		return data
		

	def form_valid(self, form):
		print('HI')
		context = self.get_context_data()
		titles = context['titles']
		with transaction.atomic():
			print('sdfsdf')
			form.instance.user = self.request.user
			print(form)
			self.object = form.save() 

			if titles.is_valid():
				titles.instance.user = self.request.user
				titles.instance = self.object
				titles.save()

			# for title in titles:
					# print(title.prefix)
				# print(titles)
		return super(CycleTransactionCreate, self).form_valid(form)
def saveData(request):
	return render(request, 'cycle_form.html')

    
def CycleTransactionGet(request):
  if request.method == "GET":

    print(request.GET.get('objectives_trans'))
    cc = request.GET.get('objectives_trans')
    print(cc)
    # cycle_id = Cycle.objects.get(cycle_name=cc).id

    objectives_trans = Objectives.objects.filter(cycle__cycle_type_id=cc)
    print(objectives_trans)

  return HttpResponse(objectives_trans)

class CycleTransactionCreateOld(CreateView):
	model = Cycle_in_obj
	fields = ['cycle_type', 'client_name']
	template_name = 'cycle_form.old.html'
	# form_class = CycleForm
	success_url = reverse_lazy('saveData')
	# queryset = Objectives.objects.all()

	def get_context_data(self, **kwargs):
		data = super(CycleTransactionCreateOld, self).get_context_data(**kwargs)

		if self.request.POST:
			data['titles'] = ObjectivesFormSet(self.request.POST)
		
		else:
			data['titles'] = ObjectivesFormSet()
		return data
		

	def form_valid(self, form):
		print('HI')
		context = self.get_context_data()
		titles = context['titles']
		with transaction.atomic():
			form.instance.user = self.request.user
			self.object = form.save()


			if titles.is_valid():
				titles.instance.user = self.request.user
				titles.instance = self.object
				titles.save()

			# for title in titles:
					# print(title.prefix)
				# print(titles)
		return super(CycleTransactionCreateOld, self).form_valid(form)


"""
Given Estimate population exception rate, Tolerable exception rate, population size, the function will suggest samples.
Still to include in the function where the form data is saved in sampling model against client and cycle
"""

def sample_size(request):

	control_proceduress = Test_of_Controls.objects.all()

	if request.method == 'POST':
		
		# formset = BaseSamplingDatasheetFormset(control_proceduress=control_proceduress, data=request.POST)
		formset = SamplingForm(data=request.POST)
	
		# print(formset)
		if formset.is_valid():
			print('HI')

			data = formset.cleaned_data.get("Estimated_Population_Exception_Rate")
			data1 = formset.cleaned_data.get("Tolerable_Exception_Rate")
			# data1 = form.cleaned_data.get("Actual_Sample_Size")
			# data1 = form.cleaned_data.get("Population_Size_0")
			print(data)
			print(data1)
			return redirect ('upload_sample')
			# new_object = ICmatrix.objects.create(mxcell_id=creator_id, option=s, objectives_id=obj_id)

		else:
			print(formset.errors)
			print(formset.non_form_errors())


	else:
		control_proceduress = Test_of_Controls.objects.all()
		formset = SamplingForm()
	

	context = { 'formset' : formset }

	return render(request, 'sampling.html', context)



def sugg_samples(request):
		#population_size, margin_error=.05, confidence_level=0.99, sigma=1/2

	"""
	Calculate the minimal sample size to use to achieve a certain margin of error
	and confidence level for a sample estimate of the population mean
	
	Inputs - 
	population_size: integer
		Total size of the population that the sample is to be drawn from.

	margin_error: number
		Maximum expected difference between the true population parameter,
		suvch as mean and sample estimate

	confidence_level: If we were to draw a large number of equal samples from the population,
	the true population parametere should lie within this percentage of the intervals (sample parameter -e, sample parameter + e)
	where e is the margin for error

	Confidence level tell you how sure you can be, It is expreseed as a percetange and represents how often 
	the true percentage of the population would pick an answer lies witihin the confidence interval.

	Estimated population exception rate can be same as that of confidence_level


	sigma: number
	The standard devisation of the population. For the case of estimating a parameter in the interval [0,1]
	sigma =1/2 should be sufficient

	"""
	if request.method == "GET":
		print(request.GET.get('Population_Size'))

	formset = SamplingForm(request.POST)
	# request.session['population_size_1'] = formset.data['Population_Size']
	# print('population_size_1')
	print(request.GET.get('Population_Size'))
	EPER = float(request.GET.get('Estimated_Population_Exception_Rate', '.50'))
	print(EPER)
	TER = float(request.GET.get('Tolerable_Exception_Rate', '2'))
	print(TER)
	population = request.GET.get('Population_Size')
	
	print(population)

	alpha = 1 - (EPER)
	sigma = 1/2

	zdict = {
		.90: 1.645,
		.91: 1.695,
		.99: 2.576,
		.97: 2.17,
		.94: 1.881,
		.93: 1.812,
		.95: 1.96,
		.98: 2.326,
		.96: 2.054,
		.92: 1.751
			}

	if EPER in zdict:
		z = zdict[EPER]
	else:
		from scipy.stats import norm
		z = norm.ppf(1 - (alpha/2))
		# print(z)

		N = TER
		M = TER
			
		numerator = float(z**2 * sigma**2 * (N / (N-1)))
		# print(numerator)
		denom = M**2 + ((z**2 * sigma**2)/ (N-1))
		# print(denom)

		sample_size = float(numerator/denom)
		# print(sample_size)


	return HttpResponse(sample_size)
 



