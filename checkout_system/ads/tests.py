from django.test import TestCase
from ads.models import Product, Customer, Order, OrderItem
from decimal import Decimal


cus1 = Customer.objects.get(name="default")
cus2 = Customer.objects.get(name="UNILEVER")
cus3 = Customer.objects.get(name="APPLE")
cus4 = Customer.objects.get(name="NIKE")
cus5 = Customer.objects.get(name="FORD")
prod1 = Product.objects.get(id="classic")
prod2 = Product.objects.get(id="standout")
prod3 = Product.objects.get(id="premium")


class OrderTestCase(TestCase):

    fixtures = ['db.json']

    def test_no_discount(self):
        order1 = Order.objects.create(customer=cus1, order_ref=1)

        OrderItem.objects.create(product=prod1, order=order1)
        OrderItem.objects.create(product=prod2, order=order1)
        OrderItem.objects.create(product=prod3, order=order1)
        self.assertEqual(order1.total, Decimal('987.97'))

    def test_free_item_discount(self):
        order1 = Order.objects.create(customer=cus2, order_ref=1)

        OrderItem.objects.create(product=prod1, order=order1)
        OrderItem.objects.create(product=prod1, order=order1)
        OrderItem.objects.create(product=prod1, order=order1)
        OrderItem.objects.create(product=prod3, order=order1)

        self.assertEqual(order1.total, Decimal('934.97'))

    def test_fixed_discount(self):
        order1 = Order.objects.create(customer=cus3, order_ref=1)

        OrderItem.objects.create(product=prod2, order=order1)
        OrderItem.objects.create(product=prod2, order=order1)
        OrderItem.objects.create(product=prod2, order=order1)
        OrderItem.objects.create(product=prod3, order=order1)

        self.assertEqual(order1.total, Decimal('1294.96'))

    def test_fixed_discount_with_min_qty(self):
        order1 = Order.objects.create(customer=cus4, order_ref=1)

        OrderItem.objects.create(product=prod3, order=order1)
        OrderItem.objects.create(product=prod3, order=order1)
        OrderItem.objects.create(product=prod3, order=order1)
        OrderItem.objects.create(product=prod3, order=order1)

        self.assertEqual(order1.total, Decimal('1519.96'))
