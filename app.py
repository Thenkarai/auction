# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "auction_secret_key"

# Database Configuration
# Vercel uses a read-only filesystem; only /tmp is writable
IS_VERCEL = os.environ.get('VERCEL', False)
if IS_VERCEL:
    db_path = os.path.join('/tmp', 'auction.db')
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    db_path = os.path.join(basedir, 'instance', 'auction.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    budget = db.Column(db.Float, default=800000000.0)
    players = db.relationship('Player', backref='team', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    set_name = db.Column(db.String(50), nullable=False)
    base_price = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Available")
    price = db.Column(db.Float, default=0.0)
    credits = db.Column(db.Float, default=0.0)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

# Format Currency Filter
@app.template_filter('format_inr')
def format_inr(value):
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value

    if value >= 10000000:
        return "INR {0:.2f} Cr".format(value / 10000000.0)
    elif value >= 100000:
        return "INR {0:.2f} L".format(value / 100000.0)
    else:
        str_val = str(int(value))
        if "." in str(value):
             s = str(value).split(".")[0]
        else:
             s = str_val
             
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "INR {0}".format(r)

# Application Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/teams")
def teams():
    all_teams = Team.query.all()
    # To pass team squads
    team_data = {t.name: {"budget": t.budget, "obj": t} for t in all_teams}
    # get all sold players
    sold_players = Player.query.filter_by(status='Sold').all()
    return render_template("teams.html", teams=team_data, players=sold_players)

@app.route("/players")
def players():
    all_players = Player.query.all()
    all_teams = Team.query.all()
    return render_template("players.html", players=all_players, teams=all_teams)

@app.route("/add", methods=["GET", "POST"])
def add_player():
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        set_name = request.form["set_name"]
        base_price = request.form["base_price"]
        credits_val = float(request.form.get("credits", 0))

        new_player = Player(name=name, role=role, set_name=set_name, base_price=base_price, credits=credits_val)
        db.session.add(new_player)
        db.session.commit()

        flash(f"Player {name} added successfully!", "success")
        return redirect("/players")
    
    return render_template("add_player.html")

@app.route("/sell/<int:id>", methods=["POST"])
def sell_player(id):
    player = Player.query.get_or_404(id)
    
    if player.status != "Available":
        flash("Player already processed.", "danger")
        return redirect("/players")

    team_name = request.form["team"]
    price = float(request.form["price"])
    team = Team.query.filter_by(name=team_name).first()

    if not team:
        flash("Invalid team selected.", "danger")
        return redirect("/players")

    if team.budget < price:
        flash("Not enough budget.", "danger")
        return redirect("/players")

    team.budget -= price
    player.status = "Sold"
    player.team_id = team.id
    player.price = price

    db.session.commit()

    flash(f"{player.name} sold to {team.name} for {format_inr(price)}", "success")
    return redirect("/players")

@app.route("/unsold/<int:id>")
def unsold_player(id):
    player = Player.query.get_or_404(id)
    player.status = "Unsold"
    db.session.commit()

    flash(f"{player.name} marked as Unsold.", "warning")
    return redirect("/players")

@app.route("/undo/<int:id>", methods=["POST"])
def undo_player(id):
    player = Player.query.get_or_404(id)

    # Revert if sold
    if player.status == "Sold" and player.team_id:
        team = Team.query.get(player.team_id)
        if team:
            team.budget += player.price # Refund the budget
            flash(f"Undid sale of {player.name}. {format_inr(player.price)} refunded to {team.name}.", "info")
    elif player.status == "Unsold":
        flash(f"Undid 'Unsold' status of {player.name}.", "info")
    else:
        flash("Player is already Available.", "warning")
        return redirect("/players")

    # Reset player attributes
    player.status = "Available"
    player.team_id = None
    player.price = None
    db.session.commit()

    return redirect("/players")

@app.route("/delete/<int:id>", methods=["POST"])
def delete_player(id):
    player = Player.query.get_or_404(id)

    # If the player was sold, refund the team's budget
    if player.status == "Sold" and player.team_id:
        team = Team.query.get(player.team_id)
        if team:
            team.budget += player.price
            flash(f"Refunded {format_inr(player.price)} to {team.name} for removing {player.name}.", "info")

    db.session.delete(player)
    db.session.commit()

    flash(f"Player {player.name} has been removed from the auction pool.", "success")
    return redirect("/players")

# Initialize DB command
def init_db():
    with app.app_context():
        db.create_all()
        # Create default teams if they don't exist
        if not Team.query.first():
            default_teams = [
                "Chennai Super Kings (CSK)",
                "Mumbai Indians (MI)",
                "Royal Challengers Bengaluru (RCB)",
                "Kolkata Knight Riders (KKR)",
                "Sunrisers Hyderabad (SRH)",
                "Delhi Capitals (DC)",
                "Rajasthan Royals (RR)",
                "Punjab Kings (PBKS)"
            ]
            for name in default_teams:
                team = Team(name=name)
                db.session.add(team)
            db.session.commit()
            print("Database initialized with default teams.")

# Initialize DB on module load (required for Vercel cold starts)
init_db()

if __name__ == "__main__":
    app.run(debug=True)
