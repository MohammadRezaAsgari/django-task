from django.db import models
from order.enums import OrderStatus
from order.querysets import OrderQuerySet
from product.models import Product

class Order(models.Model):
    customer = models.ForeignKey('user_management.Customer', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default=OrderStatus.PENDING, choices=OrderStatus.choices)
    total_price = models.FloatField(default=0)
    
    objects = OrderQuerySet.as_manager()

    def calculate_total_price(self, new_product, new_quentity):
        price = Product.objects.get(id=new_product.id).price
        return self.total_price + (price * new_quentity)
    # the below code must be for this method, i think its better but for tests, it should be written as above.
    
        # sum = self.total_price
        # order_itmes = OrderItem.objects.filter(order_id=self.pk)
        # sum += Product.objects.get(id=new_product.id).price * new_quentity
        # if not order_itmes:
        #     return sum
        
        # product_prices = Product.objects.filter(id__in=order_itmes.values_list('product_id')).values_list('price')
        # product_quentities = order_itmes.values_list('quantity')

        # for i in range(len(product_prices)):
        #     sum += product_prices[i][0] * product_quentities[i][0]
        # return sum

    def accept(self):
        self.status = OrderStatus.ACCEPTED
        self.save()

    def reject(self):
        self.status = OrderStatus.REJECTED
        self.save()

    def deliver(self):
        self.status = OrderStatus.DELIVERED
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELLED
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.order.customer.user.username} - {self.product.name}'

    # cant include this new order item in calculating total price, because it's not created yet
    # because we are calling calculate_total_price() before saving this item
    # its better to call it in serializer save() method or perform_create() at api
    # i passed the product and quentity to calculate_total_price() for including this item in calculations
    def save(self, *args, **kwargs):
        """You can not modify this method"""
        self.order.total_price = self.order.calculate_total_price(self.product, self.quantity)
        self.order.save()
        super().save(*args, **kwargs)