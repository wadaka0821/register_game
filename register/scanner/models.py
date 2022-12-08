from django.db import models
import uuid

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return '<id : {} | name : {} | price {} | description {:20}>'.format(self.product_id,
                                                                             self.product_name,
                                                                             self.price,
                                                                             self.description)

class History(models.Model):
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_date = models.DateTimeField()
    total_price = models.PositiveBigIntegerField()
    total_product = models.PositiveIntegerField()

    def __str__(self) -> str:
        return '<id {} | purchase date {} | total price {} | total product {}>'.format(self.history_id,
                                                                                       self.purchase_date,
                                                                                       self.total_price,
                                                                                       self.total_product)

class Purchase(models.Model):
    history_id = models.ForeignKey(History, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_num = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return '<history id {} | product id {} | purchase num {}>'.format(self.history_id,
                                                                          self.product_id,
                                                                          self.purchase_num)