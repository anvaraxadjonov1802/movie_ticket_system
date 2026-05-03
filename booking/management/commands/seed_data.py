from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from django.contrib.auth.hashers import make_password

from booking.models import (
    User,
    Movie,
    Cinema,
    Hall,
    Seat,
    ShowTime,
)


class Command(BaseCommand):
    help = "Seed initial test data for Movie Ticket System"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Creating seed data..."))

        customer, _ = User.objects.update_or_create(
            email="customer@example.com",
            defaults={
                "full_name": "Test Customer",
                "password": make_password("12345"),
                "role": User.Role.CUSTOMER,
            },
        )

        admin_user, _ = User.objects.update_or_create(
            email="admin@example.com",
            defaults={
                "full_name": "Test Admin",
                "password": make_password("12345"),
                "role": User.Role.ADMIN,
            },
        )

        movie1, _ = Movie.objects.get_or_create(
            title="Avatar: The Way of Water",
            defaults={
                "description": "A science fiction movie set on Pandora.",
                "duration": 192,
                "genre": "Sci-Fi",
                "language": "English",
                "poster_url": "https://example.com/avatar.jpg",
            },
        )

        movie2, _ = Movie.objects.get_or_create(
            title="Oppenheimer",
            defaults={
                "description": "A biographical thriller film about J. Robert Oppenheimer.",
                "duration": 180,
                "genre": "Biography",
                "language": "English",
                "poster_url": "https://example.com/oppenheimer.jpg",
            },
        )

        cinema, _ = Cinema.objects.get_or_create(
            name="Magic Cinema",
            defaults={
                "address": "Tashkent City Mall",
                "city": "Tashkent",
            },
        )

        hall, _ = Hall.objects.get_or_create(
            cinema=cinema,
            name="Hall 1",
            defaults={
                "total_seats": 24,
            },
        )

        rows = ["A", "B", "C"]
        seat_count = 0

        for row in rows:
            for number in range(1, 9):
                seat_type = Seat.SeatType.REGULAR

                if row == "C":
                    seat_type = Seat.SeatType.VIP

                Seat.objects.get_or_create(
                    hall=hall,
                    row_number=row,
                    seat_number=number,
                    defaults={
                        "seat_type": seat_type,
                    },
                )
                seat_count += 1

        now = timezone.now()

        ShowTime.objects.get_or_create(
            movie=movie1,
            cinema=cinema,
            hall=hall,
            start_time=now + timedelta(days=1, hours=2),
            defaults={
                "end_time": now + timedelta(days=1, hours=5),
                "price": 50000,
            },
        )

        ShowTime.objects.get_or_create(
            movie=movie2,
            cinema=cinema,
            hall=hall,
            start_time=now + timedelta(days=2, hours=3),
            defaults={
                "end_time": now + timedelta(days=2, hours=6),
                "price": 60000,
            },
        )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully!"))
        self.stdout.write(f"Customer: {customer.email} / 12345")
        self.stdout.write(f"Admin user in app table: {admin_user.email} / 12345")
        self.stdout.write(f"Cinema: {cinema.name}")
        self.stdout.write(f"Hall: {hall.name}")
        self.stdout.write(f"Seats created/checked: {seat_count}")