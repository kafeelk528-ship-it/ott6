from flask import Flask, render_template, jsonify, request, redirect, url_for
import stripe
import os

app = Flask(__name__)

# -----------------------------------------
# ✔ Stripe Test Keys (replace with your own)
# -----------------------------------------
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_12345")

YOUR_DOMAIN = os.getenv("YOUR_DOMAIN", "https://yourrenderurl.onrender.com")


# -----------------------------------------
# ✔ Demo OTT Plans (with real logo filenames)
# -----------------------------------------
plans = [
    {
        "id": 1,
        "name": "Netflix Standard",
        "price": 199,
        "logo": "netflix.png"
    },
    {
        "id": 2,
        "name": "Amazon Prime Video",
        "price": 149,
        "logo": "prime.png"
    },
    {
        "id": 3,
        "name": "Disney+ Hotstar Premium",
        "price": 299,
        "logo": "hotstar.png"
    },
    {
        "id": 4,
        "name": "Sony LIV Premium",
        "price": 129,
        "logo": "sonyliv.png"
    },
    {
        "id": 5,
        "name": "Zee5 Premium",
        "price": 99,
        "logo": "zee5.png"
    }
]


# -----------------------------------------
# ✔ Helper to get plan by ID
# -----------------------------------------
def get_plan(plan_id):
    for p in plans:
        if p["id"] == plan_id:
            return p
    return None


# -----------------------------------------
# ✔ HOME PAGE
# -----------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------------
# ✔ PLANS PAGE
# -----------------------------------------
@app.route("/plans")
def show_plans():
    return render_template("plans.html", plans=plans)


# -----------------------------------------
# ✔ PLAN DETAILS PAGE
# -----------------------------------------
@app.route("/plan/<int:id>")
def plan_details(id):
    plan = get_plan(id)
    if plan is None:
        return "Plan Not Found", 404
    return render_template("plan-details.html", plan=plan)


# -----------------------------------------
# ✔ STRIPE CHECKOUT SESSION
# -----------------------------------------
@app.route("/create-checkout-session/<int:id>", methods=["GET", "POST"])
def create_checkout_session(id):
    plan = get_plan(id)
    if plan is None:
        return "Invalid Plan", 404

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": plan["name"]
                    },
                    "unit_amount": plan["price"] * 100,
                },
                "quantity": 1,
            }],
            mode='payment',
            success_url=f"{YOUR_DOMAIN}/success?plan={plan['id']}",
            cancel_url=f"{YOUR_DOMAIN}/plans"
        )
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return str(e)


# -----------------------------------------
# ✔ SUCCESS PAGE
# -----------------------------------------
@app.route("/success")
def success():
    plan_id = request.args.get("plan")
    plan = get_plan(int(plan_id)) if plan_id else None
    return render_template("success.html", plan=plan)


# -----------------------------------------
# ✔ CONTACT PAGE
# -----------------------------------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# -----------------------------------------
# ✔ ADMIN PAGE (DEMO ONLY)
# -----------------------------------------
@app.route("/admin")
def admin():
    return render_template("admin.html", plans=plans)


# -----------------------------------------
# ✔ RUN APP
# -----------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
