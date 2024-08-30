from flask import Flask, jsonify, request
import psycopg2

DB_CONFIG = {
    'host': "aws-0-ap-south-1.pooler.supabase.com",
    'database': "postgres",
    'user': "postgres.fayafjrwupqupjltsdeg",
    'password': "@Satwikkr055"
}

connection = psycopg2.connect(**DB_CONFIG)
cursor = connection.cursor()
app = Flask(__name__)


@app.route('/bookings/<int:user_id>', methods=['GET'])
def get_all_bookings(user_id):
    try:

        cursor.callproc('get_all_bookings', [user_id])
        response = cursor.fetchone()

        if response is None:
            raise Exception(f"No booking available of {user_id} type")

        else:
            columns = [desc[0] for desc in cursor.description]
            response_dict = dict(zip(columns, response))
            properties = [response_dict]
            return jsonify(properties)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/booking/<int:booking_id>', methods=['GET'])
def get_booking_by_id(booking_id):
    try:
        cursor.callproc('get_booking_by_id', [booking_id])

        response = cursor.fetchone()

        if response is None:
            return jsonify({"error": f"No booking with id {booking_id} found"}), 400
        else:
            columns = [desc[0] for desc in cursor.description]
            response_dict = dict(zip(columns, response))
            return jsonify(response_dict)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/hello', methods=['GET'])
def hello():
    return "Hi from booking service"


if __name__ == '__main__':
    app.run()
