from django.db import models


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
