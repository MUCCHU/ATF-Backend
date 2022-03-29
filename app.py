from flask import Flask, request
from connection import connection, cursor
import json

app = Flask(__name__)


@app.route("/")
def handler():
    response = ['/earn, POST, amount, user_id, jwt, earn coins after purchase according to amount',
                '/redeem, POST, count | user_id | jwt , redeem coins to real amount before purchase',
                '/feedbacks/ , GET,  , List Feedbacks',
                '/feedbacks/ , POST,  user_id | entry_id | description | rating , Create a Feedback',
                '/feedbacks/<int:feedback_id> , GET,   , Show a feedback',
                '/feedbacks/<int:feedback_id> , POST,  user_id | entry_id | description | rating | remarks , Update a feedback',
                '/feedbacks/<int:feedback_id> , DELETE,   , Delete a feedback']
    return json.dumps(response)


# Loyalty Points
@app.route("/earn", methods=['POST'])
def earn():
    amount = int(request.form.get("amount"))
    user_id = request.form.get("user_id")
    count = amount / 50

    cursor.execute("UPDATE users SET loyalty_pts=loyalty_pts+%s WHERE user_id=%s", (count, user_id))

    if cursor:
        connection.commit()
        cursor.execute("SELECT loyalty_pts FROM feedbacks WHERE user_id=%s", (user_id,))
        response = {
            "success": 1,
            "amount_of_purchase": amount,
            "points_added": count,
            "current_lp": cursor.fetchone()[0]
        }
    else:
        connection.commit()
        response = {
            "success": 0,
        }

    return json.dumps(response)


@app.route("/redeem", methods=['POST'])
def redeem():
    count = request.form.get("count")
    user_id = request.form.get("user_id")

    cursor.execute("UPDATE users SET loyalty_pts=loyalty_pts-%s WHERE user_id=%s", (count, user_id))

    if cursor:
        connection.commit()
        cursor.execute("SELECT loyalty_pts FROM feedbacks WHERE user_id=%s", (user_id,))
        response = {
            "success": 1,
            "amount_equivalent": count * 5,
            "count_redeemed": count,
            "current_lp": cursor.fetchone()[0]
        }
    else:
        connection.commit()
        response = {
            "success": 0,
        }

    return json.dumps(response)


# feedbacks
@app.route('/feedbacks/', methods=['GET', 'POST'])
def index():
    # List all feedbacks
    if request.method == "GET":
        cursor.execute("SELECT * FROM feedbacks;")
        feedbacks = []
        for feedback in cursor:
            feedbacks.append(feedback)
        return json.dumps(feedbacks)

    # Create a feedback
    elif request.method == "POST":
        user_id = request.form.get("user_id")
        entry_id = request.form.get("entry_id")
        description = request.form.get('description')
        rating = request.form.get('rating')
        cursor.execute(
            "INSERT INTO feedbacks (user_id, entry_id, description, rating, created_at, remarks) VALUES (%s,%s,%s,%s,NOW(), NULL);",
            (user_id, entry_id, description, rating,))

        connection.commit()
        return json.dumps({'success: 1'})


@app.route('/feedbacks/<int:feedback_id>', methods=['GET', 'POST', 'DELETE'])
def fetch(feedback_id):
    cursor.execute("SELECT * FROM feedbacks WHERE feedback_id=%s", (feedback_id,))
    feedback = cursor.fetchone()

    # Show a feedback
    if request.method == 'GET':
        return json.dumps(feedback)

    # Update feedback
    elif request.method == 'POST':
        user_id = request.form.get("user_id") if request.form.get("user_id") else feedback[1]
        entry_id = request.form.get("entry_id") if request.form.get("entry_id") else feedback[2]
        description = request.form.get('description') if request.form.get("description") else feedback[3]
        rating = request.form.get('rating') if request.form.get("rating") else feedback[4]
        remarks = request.form.get('remarks') if request.form.get("remarks") else feedback[6]

        cursor.execute(
            "UPDATE feedbacks SET user_id=%s, entry_id=%s, description=%s, rating=%s, remarks=%s WHERE feedback_id=%s",
            (user_id, entry_id, description, rating, remarks, feedback_id)
        )

        connection.commit()
        return json.dumps({
                "success": 1
            })

    # Delete feedbacks
    elif request.method == "DELETE":
        cursor.execute(
            "DELETE FROM feedbacks WHERE feedback_id=%s",
            (feedback_id,)
        )
        if cursor:
            response = {
                "success": 1
            }
        else:
            response = {
                "success": 0
            }
        connection.commit()
        return json.dumps(response)


if __name__ == '__main__':
    app.run()
