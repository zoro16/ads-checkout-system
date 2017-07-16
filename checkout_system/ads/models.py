from django.db import models


class Customer(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.CharField(
        max_length=200,
        primary_key=True,
    )
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.id


class Discount(models.Model):
    for_every_qty_items = models.IntegerField(null=True, blank=True)
    free_items = models.IntegerField(null=True, blank=True)
    fixed_discount = models.DecimalField(
        null=True,
        blank=True,
        max_digits=6,
        decimal_places=2
    )
    min_qty_before_fixed_discount = models.IntegerField(null=True, blank=True)

    customer = models.ManyToManyField(Customer)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.id


class PricingRules:
    def get_discount(self, customer, product):
        return Discount.objects.filter(customer__name=customer, product=product)

    def check_free_items_discount(self, for_every_qty_items, free_items):
        if for_every_qty_items is not None and free_items is not None:
            return True
        return False

    def check_fixed_discount(self, fixed_discount, min_qty_before_fixed_discount):
        if fixed_discount is not None and min_qty_before_fixed_discount is None:
            return True
        return False

    def check_fixed_discount_with_min_qty(self, fixed_discount, min_qty_before_fixed_discount):
        if min_qty_before_fixed_discount is not None:
            return True
        return False

    def calculate_fixed_discount(self, price, fixed_discount):
        return price - fixed_discount

    def calculate_fixed_discount_with_min_qty(self,
                                              min_qty_counter,
                                              fixed_discount,
                                              min_qty_before_fixed_discount,
                                              price):
        if min_qty_counter == min_qty_before_fixed_discount:
            total_discount = min_qty_counter * fixed_discount
            return price - total_discount

        if min_qty_counter > min_qty_before_fixed_discount:
            return price - fixed_discount

        return price

    def calculate_free_items_discount(self, qty_counter, for_every_qty_items, total_price, price):
        if qty_counter % for_every_qty_items == 0:
            return total_price
        total_price += price
        return total_price


class Order(PricingRules, models.Model):
    order_ref = models.PositiveSmallIntegerField(default=1)
    products = models.ManyToManyField(Product, through='OrderItem')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=6, decimal_places=2, editable=False)

    @property
    def total(self):
        final_total = 0
        qty_counter = 1
        min_qty_counter = 1
        rules = PricingRules()

        for product in self.products.all():
            discount = rules.get_discount(self.customer.name, product.id)

            if discount.count() > 0:
                free_items = discount[0].free_items
                for_every_qty_items = discount[0].for_every_qty_items
                fixed_discount = discount[0].fixed_discount
                min_qty_before_fixed_discount = discount[0].min_qty_before_fixed_discount

                if rules.check_free_items_discount(for_every_qty_items, free_items):
                    final_total = rules.calculate_free_items_discount(qty_counter,
                                                                      for_every_qty_items,
                                                                      final_total,
                                                                      product.price)
                    qty_counter += 1

                if rules.check_fixed_discount(fixed_discount, min_qty_before_fixed_discount):
                    final_total += rules.calculate_fixed_discount(product.price, fixed_discount)

                if rules.check_fixed_discount_with_min_qty(fixed_discount,
                                                           min_qty_before_fixed_discount):
                    final_total += rules.calculate_fixed_discount_with_min_qty(min_qty_counter,
                                                                               fixed_discount,
                                                                               min_qty_before_fixed_discount,
                                                                               product.price)
                    min_qty_counter += 1

            else:
                final_total += product.price

        return final_total

    def __str__(self):
        return self.order_ref


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    
