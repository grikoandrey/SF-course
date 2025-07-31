from django.db import models
from django.utils import timezone
from .resources import POSITIONS


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    pickup = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField('Product', through='ProductOrder')

    def finish_order(self):
        self.time_out = timezone.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete and self.time_out:
            return (self.time_out - self.time_in).total_seconds() // 60
        else:
            return (timezone.now() - self.time_in).total_seconds() // 60


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)


class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default='CA')
    labor_contract = models.IntegerField(default=0)

    def get_last_name(self):
        return self.full_name.split()[0]


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    in_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column='amount')

    def product_sum(self):
        product_price = self.product.price
        return product_price * self._amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()
