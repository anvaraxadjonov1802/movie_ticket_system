from django.urls import path
from .views import (
    MovieListView,
    MovieDetailView,
    CinemaListView,
    ShowTimeByMovieView,
    ShowTimeSeatAvailabilityView,
    CreateBookingView,
    BookingDetailView,
    UserBookingsView,
    CreatePaymentView,
    BookingTicketsView,
)


urlpatterns = [
    path("movies/", MovieListView.as_view(), name="movie-list"),
    path("movies/<int:movie_id>/", MovieDetailView.as_view(), name="movie-detail"),

    path("cinemas/", CinemaListView.as_view(), name="cinema-list"),

    path(
        "movies/<int:movie_id>/showtimes/",
        ShowTimeByMovieView.as_view(),
        name="movie-showtimes"
    ),

    path(
        "showtimes/<int:showtime_id>/seats/",
        ShowTimeSeatAvailabilityView.as_view(),
        name="showtime-seats"
    ),

    path("bookings/", CreateBookingView.as_view(), name="create-booking"),
    path("bookings/<int:booking_id>/", BookingDetailView.as_view(), name="booking-detail"),
    path("users/<int:user_id>/bookings/", UserBookingsView.as_view(), name="user-bookings"),

    path("payments/", CreatePaymentView.as_view(), name="create-payment"),

    path(
        "bookings/<int:booking_id>/tickets/",
        BookingTicketsView.as_view(),
        name="booking-tickets"
    ),
]