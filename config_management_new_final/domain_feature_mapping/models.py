from django.db import models
from domains.models import Domain
from features.models import Feature

# Create your models here.
class DomainFeatureMapping(models.Model):
	domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
	feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('domain', 'feature'),)

	def __str__(self):
		return "domain%s---feature%s" % (str(self.domain), str(self.feature))
