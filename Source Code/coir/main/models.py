from django.db import models

# Create your models here.
class industryRequirement(models.Model):
    industryName = models.CharField(max_length=50)
    materialType = models.CharField(max_length=50)
    priceOffered = models.IntegerField()
    quantityRequired = models.IntegerField()
    
    class Meta:
        unique_together = ('industryName', 'materialType') 
    
class farmerRequest(models.Model):
    farmerName = models.CharField(max_length=50)
    industryName = models.CharField(max_length=50)
    materialType = models.CharField(max_length=50)
    priceOffered = models.IntegerField(default=0)
    quantityAvailable = models.IntegerField()
    phoneNumber = models.PositiveBigIntegerField()
    upiID = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    
    class Meta:
        unique_together = ('farmerName', 'industryName', 'materialType')
    
class feedbacks(models.Model):
    userType = models.CharField(max_length=15)
    feedback = models.CharField(max_length=1000)
    
class transactions(models.Model):
    txn_id = models.CharField(max_length=30)
    farmerName = models.CharField(max_length=50)
    industryName = models.CharField(max_length=50)
    materialType = models.CharField(max_length=50)
    quantity = models.IntegerField()
    amount = models.IntegerField()
    ss = models.FileField()
    Date = models.DateTimeField(auto_now_add=True)
