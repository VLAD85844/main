from django.db import models


class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        total = sum(item.item.price * item.quantity for item in self.orderitem_set.all())
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Discount(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='discount')
    percent_off = models.DecimalField(max_digits=5, decimal_places=2)
    name = models.CharField(max_length=100)


class Tax(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tax')
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    display_name = models.CharField(max_length=100)
    inclusive = models.BooleanField(default=False)