from celery.schedules import crontab
from application.workers import celery
from datetime import datetime
from flask import current_app as app
from application.model import *
from datetime import date, datetime, timedelta   
from sqlalchemy import func
import os

from jinja2 import Template
import pdfkit

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import csv

from flask_security import current_user


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = "25"
SENDER_ADDRESS = "admin@ticketshow.com"
SENDER_PASSWORD = ""

# print("crontab ", crontab)

def data_for_monthly_report(current_user_id):

    # Date range of previous month
    today = datetime.today().date()
    past_month_end = today.replace(day=1) - timedelta(days=1)
    past_month_start = past_month_end.replace(day=1)


    # Get bookings made by the user in the past month
    bookings_past_month = Booking.query.filter_by(user_id=current_user_id) \
                                       .filter(Booking.booking_time >= past_month_start) \
                                       .filter(Booking.booking_time <= past_month_end) \
                                       .all()
                                       
    # return ( str(past_month_start))
    if bookings_past_month != []:
        # Calculate the number of bookings and total amount spent
        booking_count = len(bookings_past_month)
        total_amount_spent = sum(booking.show.price * booking.no_of_tickets for booking in bookings_past_month)

        # Find the most visited venue
        venue_id_counts = {}
        for booking in bookings_past_month:
            venue_id = booking.show.venue_id
            venue_id_counts[venue_id] = venue_id_counts.get(venue_id, 0) + 1
        # print(venue_id_counts)
    
        most_visited_venue_id = max(venue_id_counts, key=venue_id_counts.get)
        most_visited_venue = Venue.query.get(most_visited_venue_id)

        booking_details = []
        for booking in bookings_past_month:
            show = Show.query.get(booking.show_id)
            venue = Venue.query.get(show.venue_id)
            
            booking_info = {
                'booking_id': booking.booking_id,
                'rating': booking.rating,
                'amount_spent': booking.show.price * booking.no_of_tickets,
                'place': venue.place if venue else None,
                'venue': venue.Vname if venue else None,
                'booking_timing': booking.booking_time
                # Add more details as needed
            }
            booking_details.append(booking_info)

        report_data = {
            'booking_count': booking_count,
            'total_amount_spent': total_amount_spent,
            'most_visited_venue': most_visited_venue.Vname,
            'booking_details': booking_details
        }

        return report_data
    else:
        return ("Oh no!! No bookings made in the past month.")


def data_for_daily_reminder(current_user_id):

    today = date.today()

    bookings_today = Booking.query.filter_by(user_id=current_user_id).filter(Booking.booking_time >= today).count()
    if bookings_today > 0:
        return False
    else:
        return True

    
    
def data_for_venue_export(venue_id):

    venue = Venue.query.get(venue_id)
    if not venue:
        return None

    shows_data = []

    for show in venue.shows:
        num_bookings = Booking.query.filter_by(show_id=show.show_id).count()
        avg_rating = db.session.query(func.avg(Booking.rating)).filter_by(show_id=show.show_id).scalar()
        total_tickets_booked = db.session.query(func.sum(Booking.no_of_tickets)).filter_by(show_id=show.show_id).scalar()
        shows_data.append({
            'show_id': show.show_id,
            'show_name': show.Sname,
            'num_bookings': num_bookings,
            'avg_rating': avg_rating,
            'total_tickets_booked': total_tickets_booked
        })

    return shows_data

def send_email(to_address, subject, message, attachment_file=""):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    if attachment_file != "":

        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment_file}"
        )

        msg.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True


def generate_content_for_monthly_report_and_send_mail(data, email, html_pdf):
    # # Get the directory path where the tasks.py script is located
    # script_directory = os.path.dirname(os.path.abspath(__file__))

    # # Create the absolute path for the monthly_report.html file
    # template_path = os.path.join(script_directory, "application", "monthly_report.html")

    with open("C:\\Users\\HP\\21f1006310\\Ticketly\\backend\\application\\monthly_report.html") as file_:
        template = Template(file_.read())
        message = template.render(report_data=data)
        
        if html_pdf == "HTML":
            send_email(email, subject="Monthly Report",
                   message=message)
        elif html_pdf == "PDF":
            file_name = 'monthly_report.pdf'
            pdfkit.from_string(message, file_name)

            send_email(email, subject="Monthly Report",
                    message="Please find the attached Monthly Report", attachment_file=file_name)

        return str(True)



def generate_content_for_venue_export_and_send_mail(data, email):
    
    csv_filename = "data.csv"

    # Extract the field names from the first dictionary
    field_names = data[0].keys()

    # Write the data to the CSV file
    with open(csv_filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(data)
    
    send_email(email, subject="Venue Data",
            message="Please find the attached Venue data", attachment_file=csv_filename)

    return str(True)


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(0, 0, day_of_month='1'), send_monthly_report.s(), name='1st day of every month')
    sender.add_periodic_task(
        crontab(minute=0, hour=19), send_daily_reminder.s(), name='every day 19:30')
    # sender.add_periodic_task(
    #     crontab(minute="*/1"), send_monthly_report.s(), name='1st day of every month')
    # sender.add_periodic_task(
    # crontab(minute="*/1"), send_daily_reminder.s(), name='every day 19:30')


@celery.task()
def send_monthly_report():
    users = User.query.all()
    for user in users:
        desired_role = 'user'
        has_desired_role = any(role.name == desired_role for role in user.roles)

        if has_desired_role:
            data = data_for_monthly_report(user.id)
            generate_content_for_monthly_report_and_send_mail(data, user.email, user.html_pdf)
    return True

# If the User has not booked anything, send him a reminder to book]

@celery.task()
def send_daily_reminder():
    users = User.query.all()
    for user in users:
        desired_role = 'user'
        has_desired_role = any(role.name == desired_role for role in user.roles)

        if has_desired_role:
            has_not_booked = data_for_daily_reminder(user.id)
            if has_not_booked:
                send_email(user.email, "Daily Reminder", "You haven't booked any ticket today!!!")
    return True


@celery.task()
def export_venue_summary(venue_id, user_id):
    user = User.query.filter_by(id = user_id).first()
    data = data_for_venue_export(venue_id)
    generate_content_for_venue_export_and_send_mail(data, user.email)
    print(user.email)
    return(user.email)
    return "True", 200


# celery -A app.celery beat --max-interval 1 -l info
# celery -A app.celery worker -l info -P solo
# in wsl - sudo service redis-server start