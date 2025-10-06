from django.contrib import admin
from .models import Amenity, Property, PropertyPhoto, RoomType, RatePlan, InventoryCalendar
class PhotoInline(admin.TabularInline):
    model=PropertyPhoto; extra=1
class RoomTypeInline(admin.TabularInline):
    model=RoomType; extra=1
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display=('id','name','city','rating','base_price','discount_percent')
    list_filter=('city','category')
    search_fields=('name','address')
    inlines=[PhotoInline, RoomTypeInline]
admin.site.register(Amenity)
admin.site.register(PropertyPhoto)
admin.site.register(RoomType)
admin.site.register(RatePlan)
admin.site.register(InventoryCalendar)
