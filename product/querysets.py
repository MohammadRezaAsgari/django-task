from django.db.models import QuerySet


class ProductQuerySet(QuerySet):
    def needs_restock(self):
        """returns a queryset of products that their stock is less than 10"""
        return self.filter(stock__lt=10)

    def in_stock(self):
        return self.filter(stock__gte=10)
