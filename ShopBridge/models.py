from django.db import models

class ProductInventory(models.Model):
    product_Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    
    class Meta:
        unique_together = ('product_Id','name')
        
    def __unicode__(self):
        return u'%s'%(self.product_Id)