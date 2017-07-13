from django.test import TestCase
from ads.models import Product, Customer, Order, OrderItem, Discount, PricingRules
from decimal import Decimal


class OrderTestCase(TestCase):
    def setUp(self):
        self.prod1 = Product.objects.create(id="classic",
                                            name="Classic Ad",
                                            price=269.99)
        self.prod2 = Product.objects.create(id="standout",
                                            name="Standout Ad",
                                            price=322.99)
        self.prod3 = Product.objects.create(id="premium",
                                            name="Premium Ad",
                                            price=394.99)

        self.cus1 = Customer.objects.create(name="default")
        self.cus2 = Customer.objects.create(name="UNILEVER")
        self.cus3 = Customer.objects.create(name="APPLE")
        self.cus4 = Customer.objects.create(name="NIKE")
        self.cus5 = Customer.objects.create(name="FORD")

    def test_fixed_discount(self):
        order1 = Order.objects.create(customer=self.cus1, order_ref=1)
        
        OrderItem.objects.create(product=self.prod1, order=order1)
        OrderItem.objects.create(product=self.prod1, order=order1)
        OrderItem.objects.create(product=self.prod1, order=order1)

        self.assertEqual(order1.total, Decimal('809.97'))
