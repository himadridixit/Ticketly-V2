from flask_restful import Resource, reqparse
from application.model import *
from application.security import *
from application.cache import *
from datetime import datetime, timedelta, date
import json
from flask import session, request
from flask_security import roles_required, login_user, auth_required, current_user
import uuid

"""
1. Add Venue: /api/venue
2. Get Venue: /api/venue/<int: venue_id>
3. Edit Venue: /api/venue/<int:venue_id>
4. Delete venue: /api/venue/<int:venue_id>
"""

create_show_parser = reqparse.RequestParser()
create_show_parser.add_argument("name", type=str)
create_show_parser.add_argument("tags", type=str)
create_show_parser.add_argument("price", type=int)
create_show_parser.add_argument("timing", type=str)
class ShowAPI(Resource):
    @auth_required('session')
    @roles_required('admin')
    def post(self, venue_id):
        args = create_show_parser.parse_args()
        show_name = args.get("name", None)
        tags = args.get("tags", None)
        price = args.get("price", None)
        timing = args.get("timing", None)
        timing_datetime = datetime.strptime(timing, "%Y-%m-%dT%H:%M")

        if show_name is None or price is None:
            return "name and price are required", 400
        
        venue = Venue.query.filter_by(venue_id = venue_id).first()

        new_show = Show(venue_id=venue_id, Sname=show_name, Tags=tags, price=price, timing=timing_datetime, tickets_remaining=venue.capacity, rating=0)
        try:
            db.session.add(new_show)
            db.session.flush()
        except Exception as e:
            print(e)
            db.session.rollback()

        db.session.commit()
        
        return {"show_id":new_show.show_id,
                "venue_id":new_show.venue_id,
                "name":new_show.Sname,
                "timing":str(new_show.timing),
                "price":new_show.price,
                "tags":new_show.Tags}, 201
    
    @auth_required('session')
    @cache.memoize(50)
    def get(self, show_id):
        show = Show.query.filter_by(show_id = show_id).first() 
        if show:
            return {
                "show_id":show.show_id,
                "name":show.Sname, 
                "timing":str(show.timing),
                "price":show.price,
                "tags":show.Tags}, 200
        else:
            return "no show found", 404
    
    @auth_required('session')
    @roles_required('admin')
    def delete(self, show_id):
        try:
            show = Show.query.get(show_id)
            if not show:
                return {"message": "Show not found"}, 404

            db.session.delete(show)
            db.session.flush()
            db.session.commit()
            
            return {"message": "Show deleted successfully"}, 200
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"message": "An error occurred while deleting the show"}, 500

    
    @auth_required('session')
    @roles_required('admin')
    def put(self, show_id):
        args = create_show_parser.parse_args()

        show_name = args.get("name", None)
        tags = args.get("tags", None)
        price = args.get("price", None)
        timing = args.get("timing", None)
        timing_datetime = datetime.strptime(timing, "%Y-%m-%d %H:%M:%S")

        show = Show.query.filter_by(show_id = show_id).first()
        if show is None:
            return "No such show", 404
        else:
            if show_name is not None:
                show.Sname = show_name
            if price is not None:
                show.price = price
            if tags is not None:
                show.Tags = tags
            if timing is not None:
                show.timing = timing_datetime
            try:
                db.session.add(show)
                db.session.flush()
            except Exception as e:
                print(e)
                db.session.rollback()
            db.session.commit()

            return {
                "show_id":show.show_id,
                "name":show.Sname,
                "timing":str(show.timing),
                "price":show.price,
                "Tags":show.Tags
                }, 201
    
     # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)
            


create_venue_parser = reqparse.RequestParser()
create_venue_parser.add_argument("name", type=str)
create_venue_parser.add_argument("place", type=str)
create_venue_parser.add_argument("capacity", type=int)

class VenueAPI(Resource):
    @auth_required('session')
    @roles_required('admin')   
    def post(self):
        args = create_venue_parser.parse_args()
        
        venue_name = args.get("name", None)
        place = args.get("place", None)
        capacity = args.get("capacity", None)

        if venue_name is None or place is None or capacity is None:
            return venue_name, 400
        
        new_venue = Venue(Vname=venue_name, place=place, capacity=capacity)
        try:
            db.session.add(new_venue)
            db.session.flush()
        except Exception as e:
            print(e)
            db.session.rollback()

        db.session.commit() 
        
        return {"venue_id":new_venue.venue_id, "name":new_venue.Vname, "place":new_venue.place, "capacity":new_venue.capacity}, 201
    
    @auth_required('session')
    @cache.memoize(50)
    def get(self, id):

        venue = Venue.query.filter_by(venue_id = id).first()

        if venue is None:
            return "No Such Venue Found", 404
        else:
            return {"venue_id":venue.venue_id, "name":venue.Vname, "place":venue.place, "capacity":venue.capacity}, 200
    
    @auth_required('session')
    @roles_required('admin')
    def delete(self, id):

        venue = Venue.query.filter_by(venue_id = id).first()
        
        if venue is None:
            return "No such venue exists", 404
        else:
            try:
                db.session.delete(venue)
                db.session.flush()
            except Exception as e:
                print(e) 
                db.session.rollback()

            db.session.commit()

            return {"venue_id": venue.venue_id}, 201
    
    @auth_required('session')
    @roles_required('admin')
    def put(self, id):

        args = create_venue_parser.parse_args()
        venuename = args.get("name", None)
        place = args.get("place", None)
        capacity = args.get("capacity", None)
        
        venue = Venue.query.filter_by(venue_id = id).first()

        if venue is None:
            return "no such venue found", 404
        else:
            if venuename is not None:
                venue.Vname = venuename
            if place is not None:
                venue.place = place
            if capacity is not None:
                venue.capacity = capacity
            try:
                db.session.add(venue)
                db.session.flush()
            except Exception as e:
                print(e)
                db.session.rollback()
            db.session.commit()
            
            return {
                    "venue_id":venue.venue_id,
                    "name":venue.Vname,
                    "place":venue.place,
                    "capacity":venue.capacity
                    }, 201
        
         # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)
    
# 201: Created
# 200: Ok
class VenuesAPI(Resource):
    @auth_required('session')
    @cache.memoize(50)
    def get(self):
        venues = Venue.query.all()
        venue_list = []
        for venue in venues:
            venue_dict = {
                "venue_id":venue.venue_id,
                "name":venue.Vname,
                "place":venue.place,
                "capacity":venue.capacity,
                "shows":[]
            }
            for show in venue.shows:
                show_dict = {
                    "show_id":show.show_id,
                    "venue_id": show.venue_id,
                    "name":show.Sname,
                    "tags":show.Tags,
                    "price":show.price,
                    "tickets_remaining":show.tickets_remaining,
                    "rating":show.rating,
                    "timing":str(show.timing)
                }
                venue_dict["shows"].append(show_dict)
            venue_dict["shows"] = list(reversed(venue_dict["shows"]))
            venue_list.append(venue_dict)
        return venue_list, 200
    
    # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)
    
create_booking_parser = reqparse.RequestParser()
create_booking_parser.add_argument("no_of_tickets", type=int)
create_booking_parser.add_argument("rating", type=int)

class BookingAPI(Resource):
    @auth_required('session')
    @roles_required('user')
    def post(self, show_id):
        user_id = current_user.id
        # print(session)
        # return 
        # # Creates a booking
        args = create_booking_parser.parse_args()
        no_of_tickets = args.get("no_of_tickets", None)

        show = Show.query.filter_by(show_id = show_id).first()
        if show.tickets_remaining >= no_of_tickets:
            booking = Booking(show_id = show_id, user_id = user_id, no_of_tickets = no_of_tickets)
            show.tickets_remaining = show.tickets_remaining - no_of_tickets
        else:
            return "Show is houseful. Please try booking another show.", 400
        try:
            db.session.add(booking)
            db.session.add(show)
            db.session.flush()
        except Exception as e:
            print(e)
            db.session.rollback()
        
        db.session.commit()
        return {
                "booking_id" : booking.booking_id,
                "user_id" : booking.user_id,
                "show_id" : booking.show_id,
                "no_of_tickets" : booking.no_of_tickets
        },  201
    
    @auth_required('session')
    @roles_required('user')
    @cache.memoize(50)
    def get(self):
        # Retrieves all the bookings
        # fs_uniquifier = session["_user_id"]
        user_id = current_user.id
        bookings = Booking.query.filter_by(user_id = user_id).all()
        booking_list = []
        for booking in bookings:
            show = Show.query.filter_by(show_id = int(booking.show_id)).first()
            venue = Venue.query.filter_by(venue_id = int(show.venue_id)).first()
            booking_dict = {
                "show_id": booking.show_id,
                "booking_id": booking.booking_id,
                "no_of_tickets": booking.no_of_tickets,
                "show_name": show.Sname,
                "venue_name": venue.Vname,
                "venue_id": venue.venue_id,
                "show_timings": str(show.timing),
                "rating": booking.rating
            }
            booking_list.append(booking_dict)
        return booking_list, 200

    @auth_required('session')
    @roles_required('user')
    def patch(self,booking_id):
        # Rates a booking
        args = create_booking_parser.parse_args()
        rating = args.get("rating", 0)
        booking = Booking.query.filter_by(booking_id = int(booking_id)).first() 
        
        if booking.rating is not None:
            return 'Bad Request', 400
        
        booking.rating = rating
        
        show = Show.query.filter_by(show_id = int(booking.show_id)).first()
        no_of_bookings = len(show.bookings)
        if show.rating is not None :
            show.rating =  ( (show.rating * (no_of_bookings-1)) + rating) / (no_of_bookings)
        else:
            show.rating = rating
        try :
            db.session.add(booking)
            db.session.add(show)
            db.session.flush()
        except Exception as e: 
            print(e)
            db.session.rollback()
        db.session.commit()

        return "Show successfully rated", 200 

         # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)   

class SearchAPI(Resource):
    @auth_required('session')
    @cache.memoize(50)
    def get(self):
        rating = request.args.get('rating')
        location = request.args.get('location')
        tags = request.args.get('tags')
        show_name = request.args.get('show_name')
        venue_name = request.args.get('venue_name')
        date = request.args.get('date')
        if rating == "" :
            rating = 0
        if location == "":
            location = "%%"
        if tags == "":
            tags = "%%"
        if show_name == "":
            show_name = "%%"
        if venue_name == "":
            venue_name = "%%" 
        if date == "":
            date = "1970-01-01"   

        selected_date = datetime.strptime(date, '%Y-%m-%d')

        # Show.query is different from db.session.query, kyunki Show.query is just a 
        shows = db.session.query(Show.show_id, Show.Sname, Show.rating, Show.Tags, Show.price, Show.timing, Show.tickets_remaining, Venue.Vname, Venue.place, Venue.venue_id, Venue.capacity).join(Venue).filter(Show.rating >= rating).filter(Venue.place.like(location)).filter(Show.Tags.ilike(tags)).filter(Show.Sname.ilike(show_name)).filter(Venue.Vname.ilike(venue_name)).filter(Show.timing >= selected_date).all()
        
        venues = {}
        
        for show in shows:
            venue_id = show.venue_id
            venue_name = show.Vname
            venue_location = show.place
            capacity = show.capacity

            if venue_id not in venues:
                venues[venue_id] = {
                    "venue_id": venue_id,
                    "name": venue_name,
                    "place": venue_location,
                    "capacity": capacity,
                    "shows": []
            }

            show_info = {
                "show_id": show.show_id,
                "name": show.Sname,
                "tags": show.Tags,
                "price": show.price,
                "tickets_remaining": show.tickets_remaining,
                "rating": show.rating,
                "timing": str(show.timing)
            }

            venues[venue_id]['shows'].append(show_info)
        
        return list(venues.values())
    
         # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)
        
class LocationAPI(Resource):
    @auth_required('session')
    @cache.memoize(50)
    def get(self):
        location_list = []
        distinct_locations = db.session.query(Venue.place).distinct().all()

        for location in distinct_locations:
            location_list.append(location[0])  # Since each distinct location is a tuple

        return location_list

    
         # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)

class TagsAPI(Resource):
    @auth_required('session')
    @cache.memoize(50)
    def get(self):
        tags_list = []
        distinct_tags = db.session.query(Show.Tags).distinct().all()
        
        for tag in distinct_tags:
            tags_list.append(tag[0])  # Since each distinct tag is a tuple
            
        return tags_list

    
         # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)
            

class GraphAPI(Resource):
    @auth_required('session')
    @cache.memoize(50)
    def get(self, venue_id):
        shows_ratings = db.session.query(
            Show.show_id,
            Show.Sname,
            Show.rating,
            Booking.rating
            ).join(Booking).filter(Show.venue_id == venue_id).all()

        # Transform the query result into a list of dictionaries
        show_dict = {}
        for show_id, sname, show_rating, booking_rating in shows_ratings:
            if show_id not in show_dict:
                show_dict[show_id] = {
                    "show_id": show_id,
                    "show_name": sname,
                    "show_rating": show_rating,
                    "booking_ratings": []
                    }
            if booking_rating != None:
                show_dict[show_id]['booking_ratings'].append(booking_rating);

        return list(show_dict.values())
    
         # Custom response for unauthorized access
    def unauthorized_response(self):
        return { "message":"Unauthorized access"}, 401

    def dispatch_request(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return self.unauthorized_response()
        return super().dispatch_request(*args, **kwargs)


login_parser = reqparse.RequestParser()
login_parser.add_argument("email", type=str)
login_parser.add_argument("password", type=str)
login_parser.add_argument("role", type=str)


class LoginAPI(Resource):
    def post(self):
        args = login_parser.parse_args()
        email = args.get("email", None)
        password = args.get("password", None)
        role = args.get("role", None)

        # Query user by email
        user = User.query.filter_by(email=email).first()

        if user is not None:
            # Check if the user has the specified role
            role_match = any(role == role_name for role_name in user.roles)
            if role_match:
                result = login_user(user)  # Assuming you have a login_user function
                if result:
                    return {"email": email, "role": role}
            else:
                return "Unauthorized", 401
        else:
            return "User not found", 404
    
register_parser = reqparse.RequestParser()
register_parser.add_argument("email", type=str, required=True)
register_parser.add_argument("password", type=str, required=True)
register_parser.add_argument("role", type=str, required=True)

class RegistrationAPI(Resource):
    def post(self):
        args = register_parser.parse_args()
        email = args.get('email', None)
        password = args.get('password', None)
        role = args.get('role', None)


        # Create the user or admin
        user_datastore.create_user(email=email, password=password, fs_uniquifier=uuid.uuid4().hex)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        role = Role.query.filter_by(name=role).first()

        user_datastore.add_role_to_user(user, role)
        db.session.commit()

        return f"{role} registered successfully", 201

preference_parser = reqparse.RequestParser()
preference_parser.add_argument("preference", type=str, required=True)
class PreferenceAPI(Resource):
    @auth_required('session')
    @roles_required('user')
    @cache.memoize(50)
    def get(self):
        user_id = current_user.id
        user = User.query.filter_by(id = user_id).first()
        return {"preference": user.html_pdf}, 200

    @auth_required('session')
    @roles_required('user')
    def patch(self):
        user_id = current_user.id
        args = preference_parser.parse_args()
        preference = args.get("preference")
        user = User.query.filter_by(id = user_id).first()
        
        user.html_pdf = preference

        try :
            db.session.add(user)
            db.session.flush()
        except Exception as e: 
            print(e)
            db.session.rollback()
        db.session.commit()

        return {"preference": user.html_pdf}, 200

