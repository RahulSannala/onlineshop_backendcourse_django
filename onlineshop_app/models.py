from django.db import models


# The TimestampModel class is an abstract model that includes fields for creation and update timestamps.
class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimestampModel):
    category_name = models.CharField(max_length=180)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.category_name


class Product(TimestampModel):
    product_name = models.CharField(max_length=180)
    description = models.TextField(max_length=180)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='products/')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.product_name


class Order(TimestampModel):
    customer_name = models.CharField(max_length=180)
    customer_email = models.EmailField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order #{self.id}"


# there above images are uploaded to products/ folder. there is no need to create this folder manuallly. when we run our migrations, this folder will be created automatically.
