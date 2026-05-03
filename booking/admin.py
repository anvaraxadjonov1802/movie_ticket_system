from django.contrib import admin
from .models import (
    User,
    Movie,
    Cinema,
    Hall,
    Seat,
    ShowTime,
    Booking,
    BookingSeat,
    Payment,
    Ticket,
)


admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Cinema)
admin.site.register(Hall)
admin.site.register(Seat)
admin.site.register(ShowTime)
admin.site.register(Booking)
admin.site.register(BookingSeat)
admin.site.register(Payment)
admin.site.register(Ticket)