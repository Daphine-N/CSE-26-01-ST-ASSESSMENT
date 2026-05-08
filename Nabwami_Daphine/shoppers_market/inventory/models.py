from django.db import models

from django.db import models

class Product(models.Model):

    product = models.CharField(max_length=100, unique=True)

    category = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=12, decimal_places=0)

    quantity = models.PositiveIntegerField()

    color = models.CharField(max_length=50)

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.product_id