from django.db.models import QuerySet
from order.models import Order
from django.db.models import Sum, Count

class CustomerQuerySet(QuerySet):
    def annotate_with_total_spending(self):
        return self.annotate(total_spending=Sum('order__total_price')).values('id', 'total_spending')

    def annotate_with_order_count(self):
        return self.annotate(order_count=Count('order__id')).values('id', 'order_count')