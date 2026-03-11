import qrcode
from io import BytesIO
from django.core.files import File
from django.core.mail import EmailMessage
from django.conf import settings

def send_ticket_email(booking):
    # 1️⃣ Generate QR data
    qr_data = f"""
Booking ID: {booking.id}
User: {booking.user.email}
Event: {booking.event.title}
Date: {booking.event.date}
"""

    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)

    # 2️⃣ Save QR to model
    booking.qr_code.save(
        f"ticket_{booking.id}.png",
        File(buffer),
        save=True
    )

    # 3️⃣ Prepare email
    email = EmailMessage(
        subject="🎟️ Event Booking Confirmed",
        body=f"""
Hi {booking.user.email},

Your booking is confirmed!

Event: {booking.event.title}
Date: {booking.event.date}
Location: {booking.event.location}

Your QR ticket is attached.
Please show it at the event entrance.

Thanks,
Event Booking Team
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[booking.user.email],
    )

    # 4️⃣ Attach QR safely
    booking.qr_code.open()
    email.attach(
        booking.qr_code.name,
        booking.qr_code.read(),
        'image/png'
    )

    # 5️⃣ Send email safely (IMPORTANT)
    try:
        email.send()
    except Exception as e:
        print("EMAIL FAILED:", e)
