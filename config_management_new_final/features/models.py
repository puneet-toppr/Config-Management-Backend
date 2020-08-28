from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

#validates if the domain name entered is in lower case on not on 'ADMIN PAGE'
def validate_case_sentitivity(string): 
	if string.islower()==True:
		return string
	else:
		raise ValidationError("Enter lower case feature name") #raise error in admin page


class Feature(models.Model): 
    name = models.CharField(max_length=200, unique=True, validators=[validate_case_sentitivity])

    def __str__(self):
        return str(self.id)

    def get_info(self):
    	return ({'name':self.name, 'id':self.id})

