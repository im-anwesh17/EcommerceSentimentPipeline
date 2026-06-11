from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .kafka_producer import publish_review_async


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField()
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_label = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review for {self.product.name} - {self.rating} stars"


@receiver(post_save, sender=Review)
def review_post_save(sender, instance, created, **kwargs):
    # Only publish to Kafka when a new review is created
    # and if it hasn't been processed yet (e.g. sentiment score is null)
    if created or (instance.sentiment_score is None and instance.sentiment_label is None):
        publish_review_async(
            review_id=instance.id,
            product_id=instance.product_id,
            text=instance.text
        )
