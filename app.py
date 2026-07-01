from flask import Flask, jsonify, request
import random
from datetime import datetime
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Enable CORS for all routes


db = pymysql.connect(
    host="localhost",
    user="root",
    password="Nish@4305",
    database="boat_booking",
    cursorclass=pymysql.cursors.DictCursor
)


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Nish@4305", 
        database="boat_booking",
        cursorclass=pymysql.cursors.DictCursor
    )
def get_all_seats():
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM seats")
        return cursor.fetchall()

api = Api(app, doc="/swagger", title="Boat Booking System API", description="API for managing boat seat bookings, meals, and predictions")
ns = api.namespace("api", description="Boat Booking APIs")

# Define models for Swagger documentation
boat_model = ns.model('Boat', {
    'boat_id': fields.String(description='Boat ID'),
    'route': fields.String(description='Boat route'),
    'stations': fields.List(fields.String, description='List of stations')
})

seat_model = ns.model('Seat', {
    'id': fields.Integer(description='Seat ID'),
    'type': fields.String(description='Seat type (Lower/Upper)'),
    'price': fields.Integer(description='Seat price'),
    'status': fields.String(description='Seat status (available/booked)'),
    'user_name': fields.String(description='Booked user name'),
    'meal_preference': fields.String(description='Meal preference')
})

health_model = ns.model('Health', {
    'status': fields.String(description='Service status'),
    'service': fields.String(description='Service name'),
    'timestamp': fields.String(description='Current timestamp')
})

booking_request = ns.model('BookingRequest', {
    'seat_id': fields.Integer(required=True, description='Seat ID to book'),
    'user_name': fields.String(required=True, description='User name')
})

booking_response = ns.model('BookingResponse', {
    'message': fields.String(description='Booking message'),
    'ticket': fields.Nested(ns.model('Ticket', {
        'seat_id': fields.Integer(description='Seat ID'),
        'passenger': fields.String(description='Passenger name'),
        'price': fields.Integer(description='Ticket price'),
        'route': fields.String(description='Boat route')
    }))
})

meal_request = ns.model('MealRequest', {
    'seat_id': fields.Integer(required=True, description='Seat ID'),
    'meal_choice': fields.String(required=True, description='Meal choice')
})

meal_response = ns.model('MealResponse', {
    'message': fields.String(description='Meal booking message'),
    'updated_ticket': fields.Nested(seat_model)
})

cancel_request = ns.model('CancelRequest', {
    'seat_id': fields.Integer(required=True, description='Seat ID to cancel')
})

cancel_response = ns.model('CancelResponse', {
    'message': fields.String(description='Cancellation message')
})

predict_request = ns.model('PredictRequest', {
    'days_left': fields.Integer(description='Days left for booking'),
    'waiting_list_pos': fields.Integer(description='Waiting list position')
})

predict_response = ns.model('PredictResponse', {
    'model_type': fields.String(description='Model type'),
    'inputs': fields.Nested(ns.model('PredictInputs', {
        'days_left': fields.Integer(description='Days left'),
        'waitlist_pos': fields.Integer(description='Waiting list position')
    })),
    'prediction_percentage': fields.Float(description='Prediction percentage'),
    'confidence_level': fields.String(description='Confidence level')
})

error_model = ns.model('Error', {
    'error': fields.String(description='Error message')
})

get_booking_response = ns.model('GetBookingResponse', {
    'seat_id': fields.Integer(description='Seat ID'),
    'passenger': fields.String(description='Passenger name'),
    'price': fields.Integer(description='Ticket price'),
    'route': fields.String(description='Boat route'),
    'meal_preference': fields.String(description='Meal preference'),
    'status': fields.String(description='Booking status')
})

# --- 1. DATA STORE (In-Memory Database) ---
# Simulating a real DB structure
boat_details = {
    "boat_id": "BOAT-101",
    "route": "Andaman Nicobar -> Lakshadweep",
    "stations": ["Port Blair", "Neil Island", "Great Nicobar", "Lakshadweep"]
}

# 20 Seats: 1-10 (Lower), 11-20 (Upper)
# Added 'price' to make it realistic

# --- 2. API ENDPOINTS ---

@app.route('/', methods=['GET'])
def health_check():
    """Simple check to see if server is running."""
    return jsonify({
        "status": "active",
        "service": "Boat Booking System",
        "timestamp": datetime.now().isoformat()
    })

@ns.route('/seats')
class SeatsResource(Resource):
    @ns.doc('get_seats')
    @ns.marshal_with(ns.model('SeatsResponse', {
        'boat_info': fields.Nested(boat_model),
        'seats': fields.List(fields.Nested(seat_model))
    }))
    def get(self):
        """Returns all seats with their current status."""
        return {
            "boat_info": boat_details,
            "seats": get_all_seats()
        }

@ns.route('/book')
class BookSeat(Resource):
    def post(self):
        data = request.json
        seat_id = data['seat_id']
        user_name = data['user_name']

        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM seats WHERE id=%s", (seat_id,))
            seat = cursor.fetchone()

            if not seat:
                return {"error": "Seat not found"}, 404

            if seat['status'] == 'booked':
                return {"error": "Seat already booked"}, 400

            cursor.execute(
                "UPDATE seats SET status='booked', user_name=%s WHERE id=%s",
                (user_name, seat_id)
            )
            db.commit()

        return {
            "ticket": {
                "seat_id": seat_id,
                "passenger": user_name,
                "price": seat['price'],
                "route": "Andaman → Lakshadweep"
            }
        }
        
        
@ns.route('/meal')
class MealResource(Resource):
    @ns.expect(meal_request)
    def post(self):
        try:
            data = request.json

            if not data or 'seat_id' not in data or 'meal_choice' not in data:
                ns.abort(400, error="Missing parameters")

            seat_id = data['seat_id']
            meal_choice = data['meal_choice']

            conn = get_db_connection()
            cursor = conn.cursor()

            # 🔍 Check seat
            cursor.execute("SELECT * FROM seats WHERE id=%s", (seat_id,))
            seat = cursor.fetchone()

            if not seat:
                ns.abort(404, error="Seat ID not found")

            if seat['status'] != 'booked':
                ns.abort(400, error="Seat not booked")

            # ✅ Update meal
            cursor.execute(
                "UPDATE seats SET meal_preference=%s WHERE id=%s",
                (meal_choice, seat_id)
            )

            conn.commit()

            # ✅ Fetch updated seat
            cursor.execute("SELECT * FROM seats WHERE id=%s", (seat_id,))
            updated_seat = cursor.fetchone()

            return {
                "message": "Meal Added Successfully",
                "updated_ticket": updated_seat
            }, 200

        except Exception as e:
            print("ERROR:", e)
            return {"error": str(e)}, 500
        
        
@ns.route('/cancel')
class CancelResource(Resource):
    @ns.doc('cancel_booking')
    def post(self):
        data = request.json
        seat_id = data.get('seat_id')

        with db.cursor() as cursor:
            # 🔍 Check seat
            cursor.execute("SELECT * FROM seats WHERE id=%s", (seat_id,))
            seat = cursor.fetchone()

            if not seat:
                return {"error": "Seat ID not found"}, 404

            if seat['status'] == 'available':
                return {"error": "Seat is not currently booked"}, 400

            # 🔄 Reset in DB
            cursor.execute(
                "UPDATE seats SET status='available', user_name=NULL, meal_preference=NULL WHERE id=%s",
                (seat_id,)
            )
            db.commit()

        return {
            "message": "Booking Cancelled. Refund Initiated.",
            "seat_id": seat_id
        }, 200
# --- 3. DATA SCIENCE MODULE (Mock Logic) ---

@ns.route('/predict')
class PredictResource(Resource):
    @ns.doc('predict_confirmation')
    @ns.expect(predict_request)
    @ns.marshal_with(predict_response)
    def post(self):
        """
        Predicts confirmation chance for a waitlisted ticket.
        Logic simulates a 'Random Forest' model behavior using weighted rules.
        """
        data = request.json
        days_left = data.get('days_left', 0)
        waitlist_pos = data.get('waiting_list_pos', 10)
        
        # 1. Base Logic: Start with 100% chance
        probability = 100.0

        # 2. Feature Impact (Coefficients simulation)
        # -5% for every person ahead in line
        probability -= (waitlist_pos * 5.0)
        # +2% for every day remaining (more time for others to cancel)
        probability += (days_left * 2.5)

        # 3. Random Noise (To simulate real-world uncertainty/AI model variance)
        # This makes the output look like a real probabilistic model, not just hard math
        noise = random.uniform(-3.0, 3.0) 
        final_score = probability + noise

        # 4. Activation Function (Clamping between 0 and 100)
        final_score = max(5.0, min(99.9, final_score))

        return {
            "model_type": "Heuristic Probabilistic Regressor",
            "inputs": {"days_left": days_left, "waitlist_pos": waitlist_pos},
            "prediction_percentage": round(final_score, 2),
            "confidence_level": "High" if final_score > 70 else "Low"
        }


@ns.route('/booking/<int:seat_id>')
class GetBookingResource(Resource):
    @ns.doc('get_booking')
    @ns.marshal_with(get_booking_response)
    @ns.response(200, 'Booking details retrieved')
    @ns.response(404, 'Booking not found', error_model)
    def get(self, seat_id):
        """Get booking details for a specific seat ID."""
        for seat in get_all_seats():
            if seat['id'] == seat_id:
                if seat['status'] != 'booked':
                    ns.abort(404, error="No booking found for this seat ID")
                
                return {
                    "seat_id": seat['id'],
                    "passenger": seat['user_name'],
                    "price": seat['price'],
                    "route": boat_details['route'],
                    "meal_preference": seat['meal_preference'],
                    "status": seat['status']
                }
        
        ns.abort(404, error="Seat ID not found")


if __name__ == '__main__':
    app.run(debug=True, port=5000)