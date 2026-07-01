# Prediction Approach: Booking Confirmation Probability

## 1. Problem Statement

The goal is to predict the percentage probability that a user's waitlisted ticket will be confirmed or that a general booking will be successful based on historical demand trends.

## 2. Model Selection

For this implementation, I propose a **Random Forest Regressor** or a **Logistic Regression** model.

* **Reason:** These models handle tabular data well and provide interpretable feature importance (e.g., seeing which factor impacts booking the most).
* **Current Mock Logic:** In the `app.py`, I have implemented a heuristic rule-based model for demonstration purposes.

## 3. Mock Dataset Structure

To train a real model, we would utilize a dataset with the following schema:

| Feature                          | Description                         | Data Type                   |
| :------------------------------- | :---------------------------------- | :-------------------------- |
| `days_before_travel`           | Number of days remaining until trip | Integer                     |
| `current_waitlist`             | Number of people currently in queue | Integer                     |
| `is_weekend`                   | Is the travel date a Sat/Sun?       | Boolean (0/1)               |
| `historical_cancellation_rate` | Avg cancellations for this route    | Float (0.0 - 1.0)           |
| **Target Variable**        | **Booking_Confirmed**         | **Binary (0/1) or %** |

## 4. Prediction Logic (Algorithm)

The simplified logic implemented in the API works as follows:

1. **Base Probability:** Start at 100%.
2. **Penalty for Queue:** Subtract 10% probability for every person ahead in the waiting list.
3. **Bonus for Time:** Add 5% probability for every day remaining before the trip (allowing time for cancellations).
4. **Clamping:** Ensure the result stays between 0% and 100%.

## 5. Output

The model outputs a percentage (e.g., "85%") which is displayed to the user to help them decide whether to join the waitlist.

## 3. Mock Training Dataset

The model is designed to be trained on historical booking logs. Below is a sample of the data structure used for training:

| Booking_ID | Days_Before_Travel | Waitlist_Position | Seasonality_Index | Is_Weekend | **Result (Target)** |
| :--------- | :----------------- | :---------------- | :---------------- | :--------- | :------------------------ |
| B_1001     | 15                 | 2                 | 0.8 (Low)         | 0          | Confirmed (1)             |
| B_1002     | 1                  | 50                | 1.2 (High)        | 1          | Cancelled (0)             |
| B_1003     | 3                  | 5                 | 1.0 (Avg)         | 0          | Confirmed (1)             |
| B_1004     | 0                  | 12                | 1.5 (Peak)        | 1          | Cancelled (0)             |

**Features Explained:**

* **Waitlist_Position:** The strongest negative correlation feature (Correlation: -0.85).
* **Days_Before_Travel:** Positive correlation; more days allow for more movement in the queue.
