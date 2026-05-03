import uuid
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as drf_status

from .models import (
    User,
    Movie,
    Cinema,
    Seat,
    ShowTime,
    Booking,
    BookingSeat,
    Payment,
    Ticket,
)
from .serializers import (
    MovieSerializer,
    CinemaSerializer,
    SeatSerializer,
    ShowTimeSerializer,
    BookingSerializer,
    CreateBookingSerializer,
    PaymentSerializer,
    CreatePaymentSerializer,
    TicketSerializer,
)


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


class CinemaListView(APIView):
    def get(self, request):
        cinemas = Cinema.objects.all()
        serializer = CinemaSerializer(cinemas, many=True)
        return Response(serializer.data)


class ShowTimeByMovieView(APIView):
    def get(self, request, movie_id):
        showtimes = ShowTime.objects.filter(movie_id=movie_id)
        serializer = ShowTimeSerializer(showtimes, many=True)
        return Response(serializer.data)


class ShowTimeSeatAvailabilityView(APIView):
    def get(self, request, showtime_id):
        showtime = get_object_or_404(ShowTime, id=showtime_id)

        seats = Seat.objects.filter(hall=showtime.hall)

        booked_seat_ids = BookingSeat.objects.filter(
            booking__show_time=showtime,
            booking__status__in=[
                Booking.BookingStatus.PENDING,
                Booking.BookingStatus.CONFIRMED,
            ],
        ).values_list("seat_id", flat=True)

        result = []

        for seat in seats:
            seat_data = SeatSerializer(seat).data
            seat_data["isAvailable"] = seat.id not in booked_seat_ids
            result.append(seat_data)

        return Response(result)


class CreateBookingView(APIView):
    def post(self, request):
        serializer = CreateBookingSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        user_id = serializer.validated_data["userId"]
        showtime_id = serializer.validated_data["showTimeId"]
        seat_ids = serializer.validated_data["seatIds"]

        if len(seat_ids) != len(set(seat_ids)):
            return Response(
                {"message": "Duplicate seat IDs are not allowed."},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)
        showtime = get_object_or_404(ShowTime, id=showtime_id)

        seats = Seat.objects.filter(
            id__in=seat_ids,
            hall=showtime.hall
        )

        if seats.count() != len(seat_ids):
            return Response(
                {"message": "Some seats are invalid for this hall."},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            already_booked = BookingSeat.objects.select_for_update().filter(
                booking__show_time=showtime,
                seat_id__in=seat_ids,
                booking__status__in=[
                    Booking.BookingStatus.PENDING,
                    Booking.BookingStatus.CONFIRMED,
                ],
            )

            if already_booked.exists():
                return Response(
                    {"message": "Some selected seats are already booked."},
                    status=drf_status.HTTP_400_BAD_REQUEST
                )

            total_amount = showtime.price * len(seat_ids)

            booking = Booking.objects.create(
                user=user,
                show_time=showtime,
                status=Booking.BookingStatus.PENDING,
                total_amount=total_amount,
            )

            booking_seats = [
                BookingSeat(
                    booking=booking,
                    seat=seat,
                    price=showtime.price
                )
                for seat in seats
            ]

            BookingSeat.objects.bulk_create(booking_seats)

        response_serializer = BookingSerializer(booking)
        return Response(
            response_serializer.data,
            status=drf_status.HTTP_201_CREATED
        )


class BookingDetailView(APIView):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)


class UserBookingsView(APIView):
    def get(self, request, user_id):
        bookings = Booking.objects.filter(user_id=user_id).order_by("-id")
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class CreatePaymentView(APIView):
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        booking_id = serializer.validated_data["bookingId"]
        payment_method = serializer.validated_data["paymentMethod"]
        payment_status = serializer.validated_data["status"]

        booking = get_object_or_404(Booking, id=booking_id)

        if booking.status != Booking.BookingStatus.PENDING:
            return Response(
                {"message": "Only PENDING bookings can be paid."},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            payment, created = Payment.objects.update_or_create(
                booking=booking,
                defaults={
                    "amount": booking.total_amount,
                    "payment_method": payment_method,
                    "status": payment_status,
                }
            )

            if payment_status == Payment.PaymentStatus.SUCCESS:
                booking.status = Booking.BookingStatus.CONFIRMED
                booking.save()

                booking_seats = BookingSeat.objects.filter(booking=booking)

                for booking_seat in booking_seats:
                    Ticket.objects.get_or_create(
                        booking=booking,
                        booking_seat=booking_seat,
                        defaults={
                            "ticket_code": self.generate_ticket_code(),
                            "qr_code": self.generate_qr_code(),
                        }
                    )

            elif payment_status == Payment.PaymentStatus.FAILED:
                booking.status = Booking.BookingStatus.CANCELLED
                booking.save()

        payment_serializer = PaymentSerializer(payment)
        ticket_serializer = TicketSerializer(
            booking.tickets.all(),
            many=True
        )

        return Response({
            "payment": payment_serializer.data,
            "tickets": ticket_serializer.data
        })

    def generate_ticket_code(self):
        return f"TKT-{uuid.uuid4().hex[:12].upper()}"

    def generate_qr_code(self):
        return f"QR-{uuid.uuid4().hex[:20].upper()}"


class BookingTicketsView(APIView):
    def get(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        tickets = Ticket.objects.filter(booking=booking)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)