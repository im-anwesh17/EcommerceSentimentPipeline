import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from reviews.models import Product

# Check if products already exist to avoid duplicates
if not Product.objects.exists():
    products = [
        Product(name="Super Wireless Headphones", description="Noise cancelling wireless over-ear headphones.", price=299.99),
        Product(name="Ergonomic Office Chair", description="Comfortable mesh chair with lumbar support.", price=199.50),
        Product(name="Mechanical Gaming Keyboard", description="RGB backlit mechanical keyboard with tactile switches.", price=89.99)
    ]
    Product.objects.bulk_create(products)
    print("Database seeded with 3 products successfully.")
else:
    print("Products already exist in the database. Seeding skipped.")
