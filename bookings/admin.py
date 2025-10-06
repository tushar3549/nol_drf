from django.contrib import admin
from .models import Booking, Guest
class GuestInline(admin.TabularInline):
    model=Guest; extra=1
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=('id','code','property','check_in','check_out','total','status')
    list_filter=('status',)
    search_fields=('code','property__name')
    inlines=[GuestInline]
admin.site.register(Guest)
