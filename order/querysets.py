from django.db.models import QuerySet
from django.db.models import Sum, Count

class OrderQuerySet(QuerySet):
    def by_customer(self, customer):
        return self.filter(customer=customer)

    def total_price(self):
        return self.values('total_price').annotate(the_sum=Sum('total_price')).values_list('the_sum')[0][0]

    def total_price_by_customer(self, customer):
        return self.filter(customer=customer).values('customer').annotate(the_sum=Sum('total_price')).values_list('the_sum')[0][0]

    def submitted_in_date(self, date_value):
        return self.filter(date=date_value)
