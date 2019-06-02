from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
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
			form.instance.user = self.request.user
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
 



