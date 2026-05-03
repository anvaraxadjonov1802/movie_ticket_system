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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "role")
    search_fields = ("full_name", "email")
    list_filter = ("role",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "duration", "genre", "language")
    search_fields = ("title", "genre", "language")


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city", "address")
    search_fields = ("name", "city")


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "cinema", "total_seats")
    search_fields = ("name", "cinema__name")
    list_filter = ("cinema",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("id", "hall", "row_number", "seat_number", "seat_type")
    search_fields = ("row_number", "seat_number")
    list_filter = ("hall", "seat_type")


@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "movie",
        "cinema",
        "hall",
        "start_time",
        "end_time",
        "price",
    )
    search_fields = ("movie__title", "cinema__name", "hall__name")
    list_filter = ("cinema", "hall", "movie")


class BookingSeatInline(admin.TabularInline):
    model = BookingSeat
    extra = 0


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "show_time", "status", "total_amount")
    search_fields = ("user__full_name", "user__email", "show_time__movie__title")
    list_filter = ("status",)
    inlines = [BookingSeatInline, TicketInline]


@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "seat", "price")
    search_fields = ("booking__id", "seat__row_number", "seat__seat_number")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "amount", "status", "payment_method")
    search_fields = ("booking__id",)
    list_filter = ("status", "payment_method")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "booking_seat", "ticket_code", "qr_code")
    search_fields = ("ticket_code", "booking__id")