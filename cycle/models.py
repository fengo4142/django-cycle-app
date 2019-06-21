from django.db import models
from picklefield.fields import PickledObjectField
import numpy


class Client(models.Model):
	client_name = models.CharField(max_length=20)
	def __str__(self):
		return self.client_name



class Cycle(models.Model):
	cycle_type = models.CharField(default='sales', max_length=15)
	client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
	# def __str__(self):
	# 	return str(self.cycle_name)
	def __str__(self):
		return str(self.cycle_type)


class Cycle_in_obj(models.Model):
	cycle_type = models.ForeignKey(Cycle, on_delete=models.CASCADE)
	#user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	client_name = models.ForeignKey(Client, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.cycle_type)



class Objectives(models.Model): #Build

	medium = 'Med'
	low = 'Low'
	high = 'High'

	Med_High_CHOICES = (
		(medium, 'Med'),
		(low, 'Low'),
		(high, 'High'),
	)

	cycle = models.ForeignKey(Cycle_in_obj, related_name="has_objectives",on_delete=models.CASCADE)
	transaction_objective = models.CharField(max_length=100)
	assessed_cr = models.CharField(max_length=20, choices = Med_High_CHOICES)




class DatafileModel(models.Model):

    data = PickledObjectField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    class Meta:
        ordering = ["updated", "pk" ]

    def __str__(self):
    	return str(self.data)

class testing_of_controls(models.Model):
	Option_CHOICES = (
    ('defecient','defecient'),
)
	data = models.ForeignKey(DatafileModel, on_delete=models.CASCADE)
	remarks = models.TextField(null=True)
	attachment = models.FileField(null=True, blank=True)
	defecient = models.CharField(max_length=8, choices=Option_CHOICES)

	def __str__(self):
		return str(self.data)


class Mxcell(models.Model): #Case
	style = models.CharField(max_length=1000)
	value = models.CharField(max_length=1000)
	# objectives = models.ManyToManyField(Objectives)
	objectives = models.ManyToManyField(Objectives)

	# XXX Cycle
	# XXX client
	# XXX get

	def __str__(self):
		return self.value
	
class Test_of_Controls(models.Model):
	mxcell = models.ForeignKey(Mxcell, on_delete=models.CASCADE)
	control_procedures = models.CharField(max_length=150)

	def __str__(self):
		return 

class sampling(models.Model):
	Estimated_Population_Exception_Rate = models.IntegerField()
	#EPER - Exception Rate that the auditor expects to find in the population 
	Tolerable_Exception_Rate = models.IntegerField() 
	#TPER - Exception Rate that the auditor will permit in the population and still be willing to conclude that -
	# - controls are operating effectively
	Population_Size = models.IntegerField()
	Suggested_Sample_Size = models.IntegerField()
	Actual_Sample_Size = models.IntegerField() #page-525
	Number_of_Exceptions = models.IntegerField(null=True)
	Sample_Exception_Rate = models.IntegerField(null=True)
	#Number of exceptions in sample divided by the sample size
	Computed_Upper_Exception_Rate = models.IntegerField(null=True)
	#The higest estimated exception rate in the population at a given ARACR
	Client = models.ForeignKey(Client, on_delete=models.CASCADE)
	Cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
	Year = models.IntegerField(null=True)

class samples(models.Model):

	samples = models.FileField(null=True, blank=True)
	Actual_Sample_Size = models.ForeignKey(Test_of_Controls, related_name="Actual_Sample_Size", on_delete=models.CASCADE)

	Random = 'Random'
	Condition = 'Condition'
	Weights = 'Weights'

	Sampling_CHOICES = (
		(Random, 'Random'),
		(Condition, 'Condition'),
		(Weights, 'Weights'),
	)
	sampling_method = models.CharField(max_length=20, choices = Sampling_CHOICES)


	def __str__(self):
		return str(self.samples)
