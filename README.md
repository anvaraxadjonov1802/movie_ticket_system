# Movie Ticket System

Movie Ticket System — foydalanuvchi kinolarni ko‘rishi, showtime tanlashi, o‘rindiq band qilishi, payment qilishi va ticket olishi uchun yaratilgan backend API loyiha.

Loyiha **Django**, **Django REST Framework** va **Swagger** yordamida qilingan.

---

## Features

- Login qilish
- Movie list ko‘rish
- Showtime ko‘rish
- Available seatlarni ko‘rish
- Bir nechta seat tanlab booking qilish
- Payment qilish
- Ticket olish
- Admin panel orqali movie, cinema, hall, seat va showtimelarni boshqarish

---

## Technologies

- Python
- Django
- Django REST Framework
- drf-spectacular
- SQLite
- Swagger UI

---

## Main Entities

Loyihadagi asosiy entitylar:

```text
User
Movie
Cinema
Hall
Seat
ShowTime
Booking
BookingSeat
Payment
Ticket
```

`BookingSeat` alohida table qilingan, chunki bitta booking ichida bir nechta seat bo‘lishi mumkin.

Masalan:

```text
Booking #1
- Seat A1
- Seat A2
- Seat A3
```

Har bir seat uchun alohida `BookingSeat` yaratiladi. Payment muvaffaqiyatli bo‘lsa, har bir `BookingSeat` uchun alohida `Ticket` yaratiladi.

---

## Project Flow

```text
1. User login qiladi.
2. User movie tanlaydi.
3. User showtime tanlaydi.
4. System available seatlarni ko‘rsatadi.
5. User bir yoki bir nechta seat tanlaydi.
6. System booking yaratadi.
7. Booking status PENDING bo‘ladi.
8. User payment qiladi.
9. Payment SUCCESS bo‘lsa booking CONFIRMED bo‘ladi.
10. Har bir seat uchun ticket yaratiladi.
```

---

## Seat Status

Seatlar 3 xil statusda bo‘lishi mumkin:

```text
AVAILABLE  - seat bo‘sh
RESERVED   - booking PENDING, payment hali qilinmagan
BOOKED     - payment SUCCESS, booking CONFIRMED
```

---

## Installation

### 1. Clone project

```bash
git clone https://github.com/anvaraxadjonov1802/movie_ticket_system.git
cd movie-ticket-system
```

`USERNAME` o‘rniga o‘zingizning GitHub username yoziladi.

---

### 2. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Install packages

```bash
pip install -r requirements.txt
```

---

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5. Create admin user

```bash
python manage.py createsuperuser
```

---

### 6. Add test data

```bash
python manage.py seed_data
```

Test user:

```text
email: customer@example.com
password: 12345
```

---

### 7. Run server

```bash
python manage.py runserver
```

Server:

```text
http://127.0.0.1:8000/
```

---

## Admin Panel

```text
http://127.0.0.1:8000/admin/
```

Admin panel orqali quyidagilarni boshqarish mumkin:

```text
User
Movie
Cinema
Hall
Seat
ShowTime
Booking
BookingSeat
Payment
Ticket
```

---

## Swagger API Documentation

Swagger:

```text
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/api/schema/
```

---

## API Endpoints

### Auth

```http
POST /api/auth/login/
```

Body:

```json
{
  "email": "customer@example.com",
  "password": "12345"
}
```

---

### Movies

```http
GET /api/movies/
GET /api/movies/{movie_id}/
```

---

### Cinemas

```http
GET /api/cinemas/
```

---

### Showtimes

```http
GET /api/movies/{movie_id}/showtimes/
```

---

### Seats

```http
GET /api/showtimes/{showtime_id}/seats/
```

---

### Booking

```http
POST /api/bookings/
GET /api/bookings/{booking_id}/
GET /api/users/{user_id}/bookings/
```

Create booking body:

```json
{
  "userId": 1,
  "showTimeId": 1,
  "seatIds": [1, 2, 3]
}
```

---

### Payment

```http
POST /api/payments/
```

Payment body:

```json
{
  "bookingId": 1,
  "paymentMethod": "CARD",
  "status": "SUCCESS"
}
```

---

### Tickets

```http
GET /api/bookings/{booking_id}/tickets/
```

---

## Test Flow

APIlarni test qilish tartibi:

```text
1. POST /api/auth/login/
2. GET /api/movies/
3. GET /api/movies/{movie_id}/showtimes/
4. GET /api/showtimes/{showtime_id}/seats/
5. POST /api/bookings/
6. GET /api/showtimes/{showtime_id}/seats/
7. POST /api/payments/
8. GET /api/bookings/{booking_id}/tickets/
```

---

## Screenshots

Agar project rasmlari yoki diagrammalar bo‘lsa, ularni `assets/` papkaga joylash mumkin.

Example:

```text
assets/swagger.png
assets/class-diagram.png
assets/system-design.png
assets/booking-flow.png
```

README ichida chiqarish:

```markdown
![Swagger](assets/swagger.png)
![Class Diagram](assets/class-diagram.png)
![System Design](assets/system-design.png)
![Booking Flow](assets/booking-flow.png)
```

---

## Current Status

Completed:

```text
Django project setup
Database models
Admin panel
Seed data command
Login API
Movie API
Cinema API
Showtime API
Seat availability API
Booking API
Payment API
Ticket API
Swagger documentation
```

---

## Author

Student: Anvar Axadjonov

Project: Movie Ticket System