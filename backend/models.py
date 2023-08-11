from django.db import models
from typing import Any, Dict
class Person(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(max_length=10, default='male')
    phone = models.CharField(max_length=20, blank=False, null=False, unique=True)
    notes = models.TextField()
    class Meta:
        app_label = 'backend'
    def __str__(self):
        return self.name
    def get_json(self,):
        return {
            'name': self.name,
            'gender': self.gender,
            'phone': self.phone,
            'notes': self.notes
        }
class Worker(Person):
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    def __init__(self, data: Dict):
        super().__init__(self, data)

class Customer(Person):
    CUSTOMER_TYPES = (
        ('relative', '亲属'),
        ('friend', '朋友'),
        ('regular', '普通客户'),
    )
    type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='regular')
    def get_json(self,):
        res = super().get_json()
        res.update({
            'type': self.type
        })
        return res


class Car(models.Model):
    license_plate = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return self.license_plate


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.id}"


class AutoPart(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    all_cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    @property
    def average_cost(self):
        return self.all_cost / self.quantity


class PurchaseOrder(models.Model):
    date = models.DateTimeField()
    supplier = models.CharField(max_length=100)

    def __str__(self):
        return f"Purchase Order {self.id}"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    auto_part = models.ForeignKey(AutoPart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    all_cost = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Item {self.id}"
    @property
    def average_cost(self):
        return self.all_cost / self.quantity

class RepairOrder(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Repair Order {self.id}"
    
class RepairOrderItem(models.Model):
    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE)
    auto_part = models.ForeignKey(AutoPart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    all_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Item {self.id}"
    @property
    def average_price(self):
        return self.all_price / self.quantity
    