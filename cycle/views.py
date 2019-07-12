from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db import DatabaseError, transaction
from django.core.files.storage import FileSystemStorage
from cycle.models import Cycle_in_obj, Objectives, Test_of_Controls, DatafileModel, sampling, Mxcell
from cycle.forms import ObjectivesForm, ObjectivesFormSet, SamplingForm, samples_form, TOC_Form, ICProcedures
import os, pandas as pd
import numpy as np
from next_prev import next_in_order, prev_in_order
from django.views.decorators.csrf import csrf_exempt


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

			obj = sampling(
				Estimated_Population_Exception_Rate = formset.cleaned_data.get("Estimated_Population_Exception_Rate"),
				Tolerable_Exception_Rate = formset.cleaned_data.get("Tolerable_Exception_Rate"),
				Suggested_Sample_Size = formset.cleaned_data.get("Suggested_Sample_Size"),
				Actual_Sample_Size = formset.cleaned_data.get("Actual_Sample_Size"),
				Population_Size = formset.cleaned_data.get("Population_Size"),
			
				Cycle = formset.cleaned_data.get("Cycle"),
				Client = formset.cleaned_data.get("Client"),
				Year = formset.cleaned_data.get("Year")
			)
			obj.save(force_insert=True)

			request.session['sampling_id'] = obj.id

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


def TOC_update(request, id=None):
	
	instance = get_object_or_404(DatafileModel, id=id)

	form = TOC_Form(request.POST or None, instance=instance)
	# the_next = instance.get_next_by_timestamp()
	newest = DatafileModel.objects.all().first()
	the_next = next_in_order(instance)
	the_prev = prev_in_order(instance)

	if form.is_valid():
		print("HI")
		# form.save()

		# data_id = DatafileModel.objects.get(data=instance).id
		defecient_selected = form.cleaned_data.get("defecient")
		remarks_selected = form.cleaned_data.get("remarks")
		new_object = testing_of_controls.objects.create(defecient=defecient_selected, remarks=remarks_selected, data_id=id)

	else:
		print(form.errors)
		# print(form.non_form_errors())
		sampling_id = request.session['sampling_id']
		#print(instance.data)
	
	
	success_url = request.get_full_path()
	print(success_url)
	context = {
    			"sampling_data": sampling.objects.get(pk=sampling_id),
    			"instance": instance,
    			"form": form,
					"the_prev": the_prev,
    			"the_next" : the_next,
    	}

	return render(request, 'sample_form.html', context)


def upload_sample(request):
    if request.method == 'POST':
    	form = samples_form(request.POST, request.FILES)
    	if form.is_valid():
    		print('HI')
    		filehandle = pd.read_csv(request.FILES['file'])
    		sampling_mtd_selected = form.cleaned_data.get("sampling_method")
    		sampling_size = form.cleaned_data.get("sampling_size")
    		sampling_id = request.session['sampling_id']
    		print(sampling_mtd_selected)

    		if sampling_mtd_selected == "Random":
    			IC_values = filehandle.sample(n=10)    			

    		# if sampling_mtd_selected == "Condition":
    		# 	Field_selected = form.cleaned_data.get("field_selected")
    		# 	field_selected_value = form.cleaned_data.get("field_selected_value")
    		# 	IC_values = filehandle[filehandle['Field_selected'] < ['field_selected_value']].sample(frac=.1).head()
    		# 	print(Field_selected)
    		# 	print(IC_values)

    		obj_id = 0    		
    		IC_values = filehandle.sample(n=10)
    		for row in IC_values.iterrows():
					
    			datafile = DatafileModel()
    			datafile.data = row
    			datafile.save()
    			if obj_id == 0:
    				obj_id = datafile.id				    			
    			# print(datafile.data)

    		object_list = DatafileModel.objects.get(id=obj_id)
    		
    		context = {
    				"object_list": object_list,
    				"IC_values": IC_values
    		}
    		return render(request, 'table.html', context)
    		# data_set.head()

    	else:
    		print(form.errors)
    else:
    	form = samples_form()
    	sampling_id = request.session['sampling_id']
    	sampling_data = sampling.objects.get(pk=sampling_id)
    return render(request, 'select_sample.html', { 'form': form, 'sampling': sampling_data })


#mxgraph


def open(request):
		return render(request, 'index.html')
@csrf_exempt 
def savefile(request):

	member_instance = request.user
	# member_instance = get_object_or_404(Member, user=user)
	print(member_instance)

	
	if request.method == "POST":
# #Get user profile
		xmlData = request.POST['xml']
		member, _ = Member.objects.get_or_create(user=member_instance)
		# member.user = member_instance;
		# member.save()
		print(member)
# #Get XML data once user presses save

def xml_to_table(request):
 	member_instance = request.user

 	result = XMLGraph.objects.all()

 	for results in result:
 		XML_response = BeautifulSoup(results.XMLGraph)
 		print(XML_response)
 		# print(XML_response.find_all('mxcell'))
 		for item in XML_response.find_all('mxcell'):
 			# print(item.get('style'))
 			# print("{}, {}".format(item.get("style"), item.get("value")))

 			data = [item.get("style"), item.get("value")]

 			k = [tuple(xi for xi in data if xi is not None)]
 			# print(k)
 			t = [yi for yi in k if yi != () ]
 			# print(t)
 			

 			for styl,val in t:
 				new_object = Mxcell.objects.create(style=styl, value=val)
 				# print(new_object)

 			IC_values = Mxcell.objects.filter(style="whiteSpace=wrap;html=1;aspect=fixed;").values('value')
 			print(IC_values)

 			table = SimpleTable(IC_values)

 	context = {

		"result": result
	
	}
 	return render(request, "table.html", {"table": table}, context)



class internal_control_procedures(CreateView):
	model = Mxcell
	template_name = 'internal_control.html'
	form_class = ICProcedures
	success_url = None
	queryset = Mxcell.objects.all()

	def get_context_data(self, **kwargs):
		
		data = super(internal_control_procedures, self).get_context_data(**kwargs)
		objective_query = Mxcell.objects.all()
		# print(data)


		if self.request.POST:
			print('HI')
			data['titles'] = BaseICProcFormset(self.request.POST)
			# print(data)
		else:
			data['titles'] = BaseICProcFormset()
		return data
		# print(data)

	def form_valid(self, form):
		print('hello')
		context = self.get_context_data()
		titles = context['titles']
		print(titles)
		with transaction.atomic():
			form.instance.created_by = self.request.user
			self.object = form.save()

			if titles.is_valid():
				titles.instance = self.object
				titles.save()
		return super(internal_control_procedures, self).form_valid(form)


	def get_success_url(self):
		return reverse('sample_size')
		
	
def saveData(request):
	return render(request, 'index.html')

    