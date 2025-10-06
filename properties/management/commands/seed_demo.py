from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from locations.models import Country, City
from properties.models import Amenity, Property, PropertyPhoto, RoomType, RatePlan
from decimal import Decimal
class Command(BaseCommand):
    help='Insert demo data for Cox\'s Bazar'
    def handle(self, *args, **kwargs):
        User=get_user_model()
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user(username='demo', password='demo123', email='demo@example.com')
        bd,_=Country.objects.get_or_create(code='BD', defaults={'name':'Bangladesh'})
        cox,_=City.objects.get_or_create(country=bd, name="Cox's Bazar", defaults={'lat':21.4272,'lng':91.9798})
        wifi,_=Amenity.objects.get_or_create(name='Free Wi-Fi', icon='wifi')
        breakfast,_=Amenity.objects.get_or_create(name='Breakfast', icon='breakfast')
        free_cancel,_=Amenity.objects.get_or_create(name='Free Cancellation', icon='cancel')
        p,_=Property.objects.get_or_create(name='Nishorgo Hotel & Resort', city=cox, defaults=dict(category='hotel', address="Marin Drive Point, Cox's Bazar, Bangladesh", lat=21.4219, lng=91.9809, rating=4.3, review_count=128, base_price=Decimal('94844.00'), discount_percent=10))
        p.amenities.set([wifi,breakfast,free_cancel])
        PropertyPhoto.objects.get_or_create(property=p, image_url='https://picsum.photos/seed/room1/800/600')
        PropertyPhoto.objects.get_or_create(property=p, image_url='https://picsum.photos/seed/room2/800/600')
        deluxe,_=RoomType.objects.get_or_create(property=p, name='Deluxe King', defaults={'max_guests':2,'beds':'1 King'})
        twin,_=RoomType.objects.get_or_create(property=p, name='Deluxe Twin', defaults={'max_guests':2,'beds':'2 Twin'})
        RatePlan.objects.get_or_create(room_type=deluxe, name='Standard', defaults={'currency':'KRW','nightly_price':Decimal('94844.00'),'breakfast_included':False,'free_cancellation':False})
        RatePlan.objects.get_or_create(room_type=deluxe, name='With Breakfast', defaults={'currency':'KRW','nightly_price':Decimal('99500.00'),'breakfast_included':True,'free_cancellation':True})
        RatePlan.objects.get_or_create(room_type=twin, name='Standard', defaults={'currency':'KRW','nightly_price':Decimal('87327.00')})
        self.stdout.write(self.style.SUCCESS('Demo data seeded ✔'))
