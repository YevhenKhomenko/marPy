from django.core.management import BaseCommand


from products.models import Product


class Command(BaseCommand):
    help = "Trasfer datat in vendor code from text to int"


        
        
    def handle(self, *args, **options):
        for product in Product.objects.all():
            product.vendor_code = len(product.vendor_code_old)
            product.save()
            print('product {} ok'.format(product.id))
            
        print('ok')
