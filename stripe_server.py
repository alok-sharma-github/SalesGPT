from flask import Flask, request, jsonify
import stripe
import os
import json

app = Flask(__name__)

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_....")

@app.route('/payment', methods=['POST'])
def create_payment():
    try:
        data = request.json

        # Ensure data contains necessary fields
        if not data or 'price_id' not in data or 'stripe_key' not in data:
            return jsonify({"error": "Invalid input"}), 400

        # Extract relevant information from the payload
        prompt = data.get("prompt")
        price_id = data.get("price_id")
        stripe_key = data.get("stripe_key")

        # Create a new Checkout Session for the order
        session = stripe.PaymentLink.create(
            # success_url="https://example.com/success",
            # cancel_url="https://example.com/cancel",
            line_items=[{
                "price": price_id,
                "quantity": 1,  # Assuming quantity 1, can be customized
            }],
            # mode="payment",
        )

        # Return the payment link to the client
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
