from rest_framework import serializers
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

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class SeatAvailabilitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    hall = serializers.IntegerField()
    row_number = serializers.CharField()
    seat_number = serializers.IntegerField()
    seat_type = serializers.CharField()
    seat_label = serializers.CharField()
    isAvailable = serializers.BooleanField()
    status = serializers.CharField()
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "role"]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "duration",
            "genre",
            "language",
            "poster_url",
        ]


class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ["id", "name", "address", "city"]


class HallSerializer(serializers.ModelSerializer):
    cinema_name = serializers.CharField(source="cinema.name", read_only=True)

    class Meta:
        model = Hall
        fields = ["id", "cinema", "cinema_name", "name", "total_seats"]


class SeatSerializer(serializers.ModelSerializer):
    seat_label = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = [
            "id",
            "hall",
            "row_number",
            "seat_number",
            "seat_type",
            "seat_label",
        ]

    def get_seat_label(self, obj):
        return f"{obj.row_number}{obj.seat_number}"


class ShowTimeSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_name = serializers.CharField(source="cinema.name", read_only=True)
    hall_name = serializers.CharField(source="hall.name", read_only=True)

    class Meta:
        model = ShowTime
        fields = [
            "id",
            "movie",
            "movie_title",
            "cinema",
            "cinema_name",
            "hall",
            "hall_name",
            "start_time",
            "end_time",
            "price",
        ]


class BookingSeatSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(read_only=True)

    class Meta:
        model = BookingSeat
        fields = ["id", "booking", "seat", "price"]


class TicketSerializer(serializers.ModelSerializer):
    seat_label = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "booking",
            "booking_seat",
            "seat_label",
            "ticket_code",
            "qr_code",
        ]

    def get_seat_label(self, obj):
        seat = obj.booking_seat.seat
        return f"{seat.row_number}{seat.seat_number}"


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    show_time = ShowTimeSerializer(read_only=True)
    booking_seats = BookingSeatSerializer(many=True, read_only=True)
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "show_time",
            "status",
            "total_amount",
            "booking_seats",
            "tickets",
        ]


class CreateBookingSerializer(serializers.Serializer):
    userId = serializers.IntegerField()
    showTimeId = serializers.IntegerField()
    seatIds = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "booking",
            "amount",
            "status",
            "payment_method",
        ]


class CreatePaymentSerializer(serializers.Serializer):
    bookingId = serializers.IntegerField()
    paymentMethod = serializers.ChoiceField(
        choices=Payment.PaymentMethod.choices
    )
    status = serializers.ChoiceField(
        choices=Payment.PaymentStatus.choices,
        required=False,
        default=Payment.PaymentStatus.SUCCESS
    )