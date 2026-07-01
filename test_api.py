import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:5000/api"

def print_test(name, result):
    print(f"[{'PASS' if result else 'FAIL'}] {name}")

def run_tests():
    print("--- Starting Automated Test Suite ---")

    # TEST 1: Get Seats (Functional)
    response = requests.get(f"{BASE_URL}/seats")
    print_test("TC_001: Fetch Seat List", response.status_code == 200)

    # TEST 2: Book a Seat (Functional)
    payload = {"seat_id": 5, "user_name": "Rahul Verma"}
    response = requests.post(f"{BASE_URL}/book", json=payload)
    print_test("TC_002: Book Seat #5", response.status_code == 201)

    # TEST 3: Add Meal (Functional - Unique Req)
    payload = {"seat_id": 5, "meal_choice": "Veg Biryani"}
    response = requests.post(f"{BASE_URL}/meal", json=payload)
    print_test("TC_003: Add Meal to Seat #5", response.status_code == 200)

    # TEST 4: Double Booking (Edge Case)
    payload = {"seat_id": 5, "user_name": "Another User"}
    response = requests.post(f"{BASE_URL}/book", json=payload)
    # Expecting 409 Conflict error
    print_test("TC_004: Prevent Double Booking", response.status_code == 409)

    # TEST 5: Meal on Unbooked Seat (Edge Case)
    payload = {"seat_id": 10, "meal_choice": "Snacks"} # Seat 10 is empty
    response = requests.post(f"{BASE_URL}/meal", json=payload)
    # Expecting 400 Bad Request
    print_test("TC_005: Prevent Meal on Empty Seat", response.status_code == 400)

    # TEST 6: Prediction API (Data Science)
    payload = {"days_left": 5, "waiting_list_pos": 2}
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    data = response.json()
    is_valid = "prediction_percentage" in data
    print_test("TC_006: AI Prediction Output", is_valid)

    # TEST 7: Get Booking by ID (Functional)
    response = requests.get(f"{BASE_URL}/booking/5")
    data = response.json()
    is_valid = response.status_code == 200 and "passenger" in data and data["passenger"] == "Rahul Verma"
    print_test("TC_007: Get Booking Details for Seat #5", is_valid)

    # TEST 8: Get Booking for Unbooked Seat (Edge Case)
    response = requests.get(f"{BASE_URL}/booking/10")
    print_test("TC_008: Get Booking for Unbooked Seat #10", response.status_code == 404)

    print("--- Testing Complete ---")

if __name__ == "__main__":
    # Ensure app.py is running in a separate terminal before running this
    try:
        run_tests()
    except Exception as e:
        print(f"Error: Server not running? {e}")