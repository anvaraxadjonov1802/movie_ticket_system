from django.db import models


class User(models.Model):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN = "ADMIN", "Admin"

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    def __str__(self):
        return f"{self.full_name} - {self.role}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Cinema(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Hall(models.Model):
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
        related_name="halls"
    )
    name = models.CharField(max_length=100)
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cinema.name} - {self.name}"


class Seat(models.Model):
    class SeatType(models.TextChoices):
        REGULAR = "REGULAR", "Regular"
        VIP = "VIP", "VIP"
        COUPLE = "COUPLE", "Couple"

    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="seats"
    )
    row_number = models.CharField(max_length=10)
    seat_number = models.PositiveIntegerField()
    seat_type = models.CharField(
        max_length=20,
        choices=SeatType.choices,
        default=SeatType.REGULAR
    )

    class Meta:
        unique_together = ("hall", "row_number", "seat_number")

    def __str__(self):
        return f"{self.hall.name} - {self.row_number}{self.seat_number}"


class ShowTime(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="showtimes"
    )
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE,
        related_name="showtimes"
    )
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="showtimes"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.movie.title} - {self.start_time}"


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    show_time = models.ForeignKey(
        ShowTime,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Booking #{self.id} - {self.user.full_name}"


class BookingSeat(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="booking_seats"
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name="booking_seats"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("booking", "seat")

    def __str__(self):
        return f"Booking #{self.booking.id} - Seat {self.seat}"


class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    class PaymentMethod(models.TextChoices):
        CARD = "CARD", "Card"
        CLICK = "CLICK", "Click"
        PAYME = "PAYME", "Payme"
        CASH = "CASH", "Cash"

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )

    def __str__(self):
        return f"Payment #{self.id} - {self.status}"


class Ticket(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    booking_seat = models.OneToOneField(
        BookingSeat,
        on_delete=models.CASCADE,
        related_name="ticket"
    )
    ticket_code = models.CharField(max_length=100, unique=True)
    qr_code = models.CharField(max_length=255)

    def __str__(self):
        return self.ticket_code