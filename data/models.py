from ExceledPandas.models import TimeStampedModel
from django.db import models


class SubDomain(models.Model):
    """
    A class which will store info about various sub domains.Related to a domain.
    - **Parameters** ::
        :param: name: Text Field: Name of the sub domain
    """
    name = models.TextField(max_length=200, unique=True)


class Domain(models.Model):
    """
    A class which will store info about various domains can relate a data or a package to.
    Domains have sub domains.
    - **Parameters** ::
        :param: name: Text Field: Name of the Domain
        :param: sub_domain: ForeignKey: To keep reference of the associated sub domain.
    """
    name = models.TextField(max_length=200)
    sub_domain = models.ManyToManyField(to=SubDomain)


class Data(TimeStampedModel):
    """
    This class stores the data which will be uploaded by the user
    -**parameter** ::

        :param: name: Name of the data
        :param: file: file associated with the data(Currently a file field)
        :param: domain: Domain of the associated data file
        :param: sub_domain: Sub Domain of the associated data file
    """
    name = models.TextField(max_length=200)
    # null true set for thinking of possibilities of database support. In that case data will be none here.
    file = models.FileField(null=True, default=None)
    """
        On deletion of reference object, we set value as All, so that we can still access the data field
        by calling it with domain filter as 'None'
    """
    domain = models.ForeignKey(to=Domain, default=None, on_delete=models.SET_DEFAULT)
    sub_domain = models.ForeignKey(to=SubDomain, default=None, on_delete=models.SET_DEFAULT)

    class Meta:
        app_label = "data"
