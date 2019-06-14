from django.db import models

"""
Still to add foregn key for client, cycle here"""
from picklefield.fields import PickledObjectField
import numpy


class DatafileModel(models.Model):

    data = PickledObjectField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    class Meta:
        ordering = ["updated", "pk" ]

    def __str__(self):
    	return str(self.data)

class Test_of_Controls(models.Model):
	Option_CHOICES = (
    ('defecient','defecient'),
)
	data = models.ForeignKey(DatafileModel, on_delete=models.CASCADE)
	remarks = models.TextField(null=True)
	attachment = models.FileField(null=True, blank=True)
	defecient = models.CharField(max_length=8, choices=Option_CHOICES)



	def __str__(self):
		return str(self.data)

class sampling(models.Model):
	control_procedures = models.ForeignKey(Test_of_Controls, on_delete=models.CASCADE)
	Estimated_Population_Exception_Rate = models.IntegerField()
	#EPER - Exception Rate that the auditor expects to find in the population 
	Tolerable_Exception_Rate = models.IntegerField() 
	#TPER - Exception Rate that the auditor will permit in the population and still be willing to conclude that -
	# - controls are operating effectively
	Population_Size = models.IntegerField()
	Suggested_Sample_Size = models.IntegerField()
	Actual_Sample_Size = models.IntegerField() #page-525
	Number_of_Exceptions = models.IntegerField()
	Sample_Exception_Rate = models.IntegerField()
	#Number of exceptions in sample divided by the sample size
	Computed_Upper_Exception_Rate = models.IntegerField()
	#The higest estimated exception rate in the population at a given ARACR


	def __str__(self):
		return str(self.control_procedures)
