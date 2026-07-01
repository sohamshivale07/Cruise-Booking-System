// API Base URL
const API_BASE = "http://127.0.0.1:5000";

// DOM Elements
const tabs = document.querySelectorAll(".tab-btn");
const tabContents = document.querySelectorAll(".tab-content");
const messagesContainer = document.getElementById("messages");

// Tab switching functionality
function showTab(tabName) {
  // Update tab buttons
  tabs.forEach((tab) => tab.classList.remove("active"));
  document
    .querySelector(`[onclick="showTab('${tabName}')"]`)
    .classList.add("active");

  // Update tab content
  tabContents.forEach((content) => content.classList.remove("active"));
  document.getElementById(`${tabName}-tab`).classList.add("active");

  // Clear results when switching tabs
  clearResults();
}

// Utility function to show messages
function showMessage(message, type = "success") {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${type}`;
  messageDiv.innerHTML = `
        <span>${message}</span>
        <button class="close-btn" onclick="this.parentElement.remove()">&times;</button>
    `;
  messagesContainer.appendChild(messageDiv);

  // Auto remove after 5 seconds
  setTimeout(() => {
    if (messageDiv.parentElement) {
      messageDiv.remove();
    }
  }, 5000);
}

// Clear all result displays
function clearResults() {
  const results = [
    "book-result",
    "meal-result",
    "cancel-result",
    "booking-result",
    "predict-result",
  ];
  results.forEach((id) => {
    const element = document.getElementById(id);
    element.style.display = "none";
    element.className = "";
    element.innerHTML = "";
  });
}

// Display result in specific container
function showResult(containerId, content, type = "success") {
  const container = document.getElementById(containerId);
  container.innerHTML = content;
  container.className = type;
  container.style.display = "block";
}

// Load and display seats
async function loadSeats() {
  try {
    const response = await fetch(`${API_BASE}/api/seats`)
    const data = await response.json();

    if (response.ok) {
      displaySeats(data.seats);
      showMessage("Seats loaded successfully!", "success");
    } else {
      showMessage("Failed to load seats", "error");
    }
  } catch (error) {
    showMessage("Error loading seats: " + error.message, "error");
  }
}

function displaySeats(seats) {
  const container = document.getElementById("seats-container");
  container.innerHTML = "";

  seats.forEach((seat) => {
    const seatCard = document.createElement("div");
    seatCard.className = `seat-card ${seat.status}`;
    seatCard.innerHTML = `
            <div class="seat-id">Seat ${seat.id}</div>
            <div class="seat-type">${seat.type}</div>
            <div class="seat-price">₹${seat.price}</div>
            ${seat.status === "booked" ? `<div class="passenger">${seat.user_name}</div>` : ""}
        `;
    container.appendChild(seatCard);
  });
}

// Book a seat
async function bookSeat(event) {
  event.preventDefault();

  const seatId = document.getElementById("book-seat-id").value;
  const userName = document.getElementById("book-user-name").value;

  try {
    const response = await fetch(`${API_BASE}/api/book`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        seat_id: parseInt(seatId),
        user_name: userName,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      showResult(
        "book-result",
        `
                <h3>Booking Confirmed!</h3>
                <p><strong>Seat ID:</strong> ${data.ticket.seat_id}</p>
                <p><strong>Passenger:</strong> ${data.ticket.passenger}</p>
                <p><strong>Price:</strong> ₹${data.ticket.price}</p>
                <p><strong>Route:</strong> ${data.ticket.route}</p>
            `,
        "success",
      );
      showMessage("Seat booked successfully!", "success");
      document.getElementById("book-form").reset();
    } else {
      showResult(
        "book-result",
        `<p><strong>Error:</strong> ${data.error}</p>`,
        "error",
      );
    }
  } catch (error) {
    showResult(
      "book-result",
      `<p><strong>Error:</strong> ${error.message}</p>`,
      "error",
    );
  }
}

// Add meal to booking
async function addMeal(event) {
  event.preventDefault();

  const seatId = document.getElementById("meal-seat-id").value;
  const mealChoice = document.getElementById("meal-choice").value;

  try {
    const response = await fetch(`${API_BASE}/api/meal`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        seat_id: parseInt(seatId),
        meal_choice: mealChoice,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      showResult(
        "meal-result",
        `<h3>Meal Added Successfully!</h3>
         <p>${data.message}</p>`,
        "success"
      );

      loadSeats(); // 🔥 refresh UI
    } else {
      showResult(
        "meal-result",
        `<p><strong>Error:</strong> ${data.error}</p>`,
        "error"
      );
    }
  } catch (error) {
    showResult(
      "meal-result",
      `<p><strong>Error:</strong> ${error.message}</p>`,
      "error"
    );
  }
}


// Cancel booking
async function cancelBooking(event) {
  event.preventDefault();

  const seatId = document.getElementById("cancel-seat-id").value;

  try {
    const response = await fetch(`${API_BASE}/api/cancel`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        seat_id: parseInt(seatId),
      }),
    });

    const data = await response.json();

    if (response.ok) {
      showResult(
        "cancel-result",
        `
                <h3>Booking Cancelled!</h3>
                <p><strong>Message:</strong> ${data.message}</p>
            `,
        "info",
      );
      showMessage("Booking cancelled successfully!", "success");
      document.getElementById("cancel-form").reset();
    } else {
      showResult(
        "cancel-result",
        `<p><strong>Error:</strong> ${data.error}</p>`,
        "error",
      );
    }
  } catch (error) {
    showResult(
      "cancel-result",
      `<p><strong>Error:</strong> ${error.message}</p>`,
      "error",
    );
  }
}

// Get booking details
async function getBooking(event) {
  event.preventDefault();

  const seatId = document.getElementById("view-seat-id").value;

  try {
    const response = await fetch(`${API_BASE}/api/booking/${seatId}`);
    const data = await response.json();

    if (response.ok) {
      showResult(
        "booking-result",
        `
                <h3>Booking Details</h3>
                <p><strong>Seat ID:</strong> ${data.seat_id}</p>
                <p><strong>Passenger:</strong> ${data.passenger}</p>
                <p><strong>Price:</strong> ₹${data.price}</p>
                <p><strong>Route:</strong> ${data.route}</p>
                <p><strong>Meal Preference:</strong> ${data.meal_preference || "None"}</p>
                <p><strong>Status:</strong> ${data.status}</p>
            `,
        "info",
      );
    } else {
      showResult(
        "booking-result",
        `<p><strong>Error:</strong> ${data.error}</p>`,
        "error",
      );
    }
  } catch (error) {
    showResult(
      "booking-result",
      `<p><strong>Error:</strong> ${error.message}</p>`,
      "error",
    );
  }
}

// Get prediction
async function getPrediction(event) {
  event.preventDefault();

  const daysLeft = document.getElementById("days-left").value;
  const waitingPos = document.getElementById("waiting-pos").value;

  try {
    const response = await fetch(`${API_BASE}/api/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        days_left: parseInt(daysLeft),
        waiting_list_pos: parseInt(waitingPos),
      }),
    });

    const data = await response.json();

    if (response.ok) {
      showResult(
        "predict-result",
        `
                <h3>Prediction Results</h3>
                <p><strong>Model Type:</strong> ${data.model_type}</p>
                <p><strong>Days Left:</strong> ${data.inputs.days_left}</p>
                <p><strong>Waiting Position:</strong> ${data.inputs.waitlist_pos}</p>
                <p><strong>Prediction:</strong> ${data.prediction_percentage}%</p>
                <p><strong>Confidence:</strong> ${data.confidence_level}</p>
            `,
        "info",
      );
      document.getElementById("predict-form").reset();
    } else {
      showResult(
        "predict-result",
        `<p><strong>Error:</strong> Failed to get prediction</p>`,
        "error",
      );
    }
  } catch (error) {
    showResult(
      "predict-result",
      `<p><strong>Error:</strong> ${error.message}</p>`,
      "error",
    );
  }
}

// Initialize the app
document.addEventListener("DOMContentLoaded", function () {
  // Load seats on page load
  loadSeats();
});
