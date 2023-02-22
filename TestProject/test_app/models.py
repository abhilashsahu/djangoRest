from django.db import models


class BaseModel(models.Model):
    """ A Reusable Class to have some common fields for multiple entity"""
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        """ Method which marks is_deleted field to true for an item in the Database """
        self.is_deleted = True
        self.save()

    def restore(self):
        """ Method which marks is_deleted field to false for an item in the Database """
        self.is_deleted = False
        self.save()

    class Meta:
        """Below snippet will make sure Django will not create
            a database table BaseModel
        """
        abstract = True


# class Company(BaseModel):
#     """ Model class for the 'Company' table creation in the Database"""
#     company_name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.company_name


class Project(BaseModel):
    """ Model class for the 'Projects' table creation in the Database"""
    id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=200)
    project_number = models.CharField(max_length=20)
    acquisition_date = models.DateField(null=True)
    number_3l_code = models.CharField(max_length=3, null=True)
    project_deal_type_id = models.CharField(max_length=20)
    project_group_id = models.CharField(max_length=20)
    project_status_id = models.CharField(max_length=20)
    # company_id = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    company_id = models.IntegerField(null=True)

    def __str__(self):
        return self.project_name


class WTG(BaseModel):
    """ Model class for the 'WTGs' table creation in the Database"""
    WTG_number = models.CharField(max_length=200)
    project_id = models.ForeignKey(Project, on_delete=models.PROTECT)
    WTG_Type_id = models.CharField(max_length=20)
    Region_id = models.CharField(max_length=40)
    kW = models.IntegerField()
    hub = models.IntegerField()
    rotor = models.IntegerField()
    altitude = models.IntegerField(null=True)
    COD = models.DateField()
    zip_code = models.IntegerField()
    WGS_84_north = models.FloatField()
    WGS_84_east = models.FloatField()
    gauss_krueger_zone = models.IntegerField()
    gauss_krueger_north = models.FloatField()
    gauss_krueger_east = models.FloatField()
    town_id = models.CharField(max_length=40)

    def __str__(self):
        return self.WTG_number
