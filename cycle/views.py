from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.db import DatabaseError, transaction
from django.core.files.storage import FileSystemStorage
from cycle.models import Cycle, Client, Cycle_in_obj, Objectives, Test_of_Controls, DatafileModel, sampling, testing_of_controls, Deficiency, Report, Mxcell, Member, XMLGraph
from cycle.forms import ObjectivesForm, ObjectivesFormSet, SamplingForm, samples_form, TOC_Form, ICProcedures, CycleInObjForm
import os, pandas as pd
import numpy as np
import json
from next_prev import next_in_order, prev_in_order

class CycleTransactionCreate(CreateView):
	model = Cycle_in_obj
	fields = ['cycle_type', 'client_name', 'year']

	template_name = 'cycle_form.html'
	# form_class = CycleForm
	success_url = reverse_lazy('grapheditor')
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
		self.request.session['cycle_in_obj'] = self.object.id

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

"""
Given Estimate population exception rate, Tolerable exception rate, population size, the function will suggest samples.
Still to include in the function where the form data is saved in sampling model against client and cycle
"""

def sample_size(request):

	control_proceduress = Test_of_Controls.objects.all()
	if 'cycle_in_obj' not in request.session:
		return redirect('') 
	cycle_in_obj = Cycle_in_obj.objects.get(id=request.session["cycle_in_obj"])

	client_name = Client.objects.get(id=cycle_in_obj.client_name_id)
	cycle_type = Cycle.objects.get(id=cycle_in_obj.cycle_type_id)
	year = cycle_in_obj.year
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
			
				Cycle = cycle_type,
				Client = client_name,
				Year = cycle_in_obj.year
			)
			obj.save(force_insert=True)

			request.session['sampling_id'] = obj.id

			return redirect ('upload_sample')
			# new_object = ICmatrix.objects.create(mxcell_id=creator_id, option=s, objectives_id=obj_id)

		else:
			print(formset.errors)


	else:
		control_proceduress = Test_of_Controls.objects.all()
		formset = SamplingForm()
	

	context = { 
		'formset' : formset,
		'cycle_type': cycle_type,
		'client_name': client_name,
		'year': year
  }

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
 

def upload_sample(request):
    sampling_id = request.session['sampling_id']
    sampling_data = sampling.objects.get(pk=sampling_id)
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
    			datafile.cycle = sampling_data.Cycle
    			datafile.client = sampling_data.Client
    			datafile.save()
    			if obj_id == 0:
    				obj_id = datafile.id				    			
    			#print(datafile.data)
    			# toc = testing_of_controls()
    			# toc.data = datafile
    			# toc.cycle = sampling_data.Cycle
    			# toc.client = sampling_data.Client
    			# toc.save()

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
    	
    return render(request, 'select_sample.html', { 'form': form, 'sampling': sampling_data })

def TOC_update(request, id=None):
	sampling_id = request.session['sampling_id']
	sampling_data = sampling.objects.get(pk=sampling_id)

	instance = get_object_or_404(DatafileModel, id=id)
	form = TOC_Form(request.POST or None, request.FILES, instance=instance)
	# the_next = instance.get_next_by_timestamp()
	cycle = sampling_data.Cycle
	client = sampling_data.Client
	newest = DatafileModel.objects.filter(cycle=cycle).filter(client=client).order_by('-id')[:10].first()
	the_next = next_in_order(instance)
	the_prev = prev_in_order(instance)
	submitted = False

	sampling_id = request.session['sampling_id']
	sampling_data = sampling.objects.get(pk=sampling_id)

	if form.is_valid() and request.method == "POST":		
		# data_id = DatafileModel.objects.get(data=instance).id
		new_object = testing_of_controls.objects.filter(data=instance).first()
		if not new_object:
			new_object = testing_of_controls()
		new_object.data = instance
		new_object.cycle = sampling_data.Cycle
		new_object.client = sampling_data.Client
		new_object.deficient = form.cleaned_data.get("deficient")
		new_object.remarks = form.cleaned_data.get("remarks") 
		new_object.save()
		submitted = True

	success_url = request.get_full_path()

	procedures = Test_of_Controls.objects.all()[:5]
	context = {
    			"sampling_data": sampling_data,
    			"instance": instance,
    			"form": form,
					"submitted": submitted,
					"procedures": procedures,
					"the_prev": the_prev,
    			"the_next" : the_next,
    	}
	return render(request, 'sample_form.html', context)


def deficiency(request):

	sampling_id = request.session['sampling_id']
	sampling_data = sampling.objects.get(pk=sampling_id)
	url = ""
	
	if request.method == "POST":
		params = request.POST

		#deficiency table submit
		if params.get("status") == "done":
			objects = list(Deficiency.objects.all())
			for obj in objects:
				obj.is_active = True
				obj.save()
			return redirect ('report_form')

		datafile = request.POST['datafile_id']
		deficiency = Deficiency.objects.filter(datafile_id=datafile).first()		

		if params.get('deficient') == 'deficient':
			is_active = True
		else:
			is_active = False

		try:
			if not deficiency:
				Deficiency.objects.create(cycle=sampling_data.Cycle, client=sampling_data.Client, remarks=params.get('remarks'), datafile_id=datafile, is_active=is_active)
			else:
				deficiency.cycle = sampling_data.Cycle
				if params.get('remarks'):
					deficiency.remarks = params.get('remarks')
				if params.get('suggestions'):
					deficiency.suggestions = params.get('suggestions')
				if params.get('financials'):
					deficiency.financials = params.get('financials')
				deficiency.is_active = is_active
				deficiency.save()
				
				if params.get('islast') == "true":
					url = reverse_lazy('deficiency')
		except Exception as e:
			print(e)
			return JsonResponse({'message' : 'failed'})
	
		return JsonResponse({'message' : 'success', 'url': url })
	else:
		sampled_deficiencies = Deficiency.objects.filter(cycle=sampling_data.Cycle).filter(client=sampling_data.Client).order_by('-id')[:10]
		deficiencies = [d for d in sampled_deficiencies if d.is_active == True]
		context = {
			"sampling_data" : sampling_data,
			"deficiencies" : deficiencies
		}
	return render(request, "deficiency.html", context)


def report_form(request):
	sampling_id = request.session['sampling_id']
	sampling_data = sampling.objects.get(pk=sampling_id)
	remarks = " ".join(filter(None, Deficiency.objects.filter(is_active=True).values_list("remarks",  flat=True)))
	financials = " ".join(filter(None, Deficiency.objects.filter(is_active=True).values_list("financials",  flat=True)))
	suggestions = " ".join(filter(None, Deficiency.objects.filter(is_active=True).values_list("suggestions",  flat=True)))
	print(remarks)
	if request.method == "POST":
		params = request.POST

		X = Report()
		X.year = sampling_data.Year
		X.client = sampling_data.Client
		X.intro_paragraph = params.get('intro_paragraph')
		X.audit_objective = params.get('audit_objective')
		X.scope_paragraph = params.get('scope_paragraph')
		X.deficiency = params.get('remarks')
		X.financials = params.get('financials')
		X.suggestions = params.get('suggestions')
		X.opinion_paragraph = params.get('opinion_paragraph')
		X.save()

		from django.http import HttpResponse
		from django.views.generic import View

		from cycle.utils import render_to_pdf 
		data = {
						'year': X.year, 
						'client': X.client,
            'intro_paragraph': X.intro_paragraph,
            'audit_objective': X.audit_objective,
            'scope_paragraph': X.scope_paragraph,
            'remarks': X.deficiency,
            'financials': X.financials,
            'suggestions': X.suggestions,
            'opinion_paragraph': X.opinion_paragraph,
		}
		pdf = render_to_pdf('pdf.html', data)
		return HttpResponse(pdf, content_type='application/pdf')

	context = {
		"sampling_data" : sampling_data,
		"remarks": remarks,
		"financials": financials,
		"suggestions": suggestions
	}

	return render(request, "report_form.html", context)



#mxgraph
def grapheditor(request):
		form = CycleInObjForm()
		context = {
			"form": form
		}
		return render(request, 'grapheditor.html', context)

def loadgraph(request):

	try:
		params = request.POST
		cycle = params.get('cycle')
		client = params.get('client')
		year = params.get('year')

		from django.db.models import Q
		ci_obj = Cycle_in_obj.objects.get(Q(client_name_id=client), Q(cycle_type_id=cycle), Q(year=year))
		xml_graph = XMLGraph.objects.filter(Q(cycle_in_obj=ci_obj)).order_by('-id')[0].XMLGraph

	except Exception as e:
		print(e)
		return JsonResponse({'message': str(e) })
	return JsonResponse({'message' : 'success', 'xml_graph': xml_graph })

@csrf_exempt 
def savegraph(request):

	member_instance = request.user
	# member_instance = get_object_or_404(Member, user=user)
	print(member_instance)

	try:
		if request.method == "POST":
		#Get user profile
			member, _ = Member.objects.get_or_create(user=member_instance)

			params = request.POST
			xmlData = params.get('xml')
			X = XMLGraph()
			X.XMLGraph = xmlData
			X.user = member_instance
			X.cycle_in_obj = request.session["cycle_in_obj"]
			X.save()

			from bs4 import BeautifulSoup
			XML_response = BeautifulSoup(X.XMLGraph)
			for item in XML_response.find_all('mxcell'):
				data = [item.get("style"), item.get("value")]
				k = [tuple(xi for xi in data if xi is not None)]
				t = [yi for yi in k if yi != () ]

				if len(t) and len(t[0]) > 1:
						for styl, val in t:
							new_object = Mxcell.objects.create(style=styl, value=val)
	#Get XML data once user presses save
	except Exception as e:
		print(e)
		return JsonResponse({'message': str(e) })
	return JsonResponse({'message' : 'success', 'xml_graph': xmlData})

def xml_to_table(request):
 	member_instance = request.user
	
 	if request.method == "POST":
			try:
				procedures = json.loads(request.POST.get("procedures"))
				for p in procedures:
					X = Test_of_Controls()
					X.control_procedures = p['value']
					X.mxcell_id = p['id']
					X.cycle_in_obj =  Cycle_in_obj.objects.get(id=request.session["cycle_in_obj"])
					X.save()
			except Exception as e:
				print(e)
				return JsonResponse({'message': str(e) })
			return JsonResponse({'message' : 'success'})
 	
 	IC_values = Mxcell.objects.filter(style__contains="whiteSpace=wrap;html=1;aspect=fixed;")
 	print(IC_values)
 			
	# table = SimpleTable(IC_values)

 	cycle_in_obj = Cycle_in_obj.objects.get(id=request.session["cycle_in_obj"])
 	client = Client.objects.get(id=cycle_in_obj.client_name_id)
 	cycle = Cycle.objects.get(id=cycle_in_obj.cycle_type_id)
 	objectives = Objectives.objects.filter(cycle_id=cycle_in_obj.id)

 	context = {
		"IC_values": IC_values,
		"cycle_type": cycle.cycle_type,
		"client_name": client.client_name,
		"year": cycle_in_obj.year,
		"objectives": objectives
	}
 	return render(request, "xmltable.html", context)



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
		
	
def returnSaveFile(request):
	return render(request, 'index.html')


def blog(request):
	return render(request, "blog.html")

def contact(request):
	return render(request, "contact.html")