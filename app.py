import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from dotenv import load_dotenv
# Load environment variables from .env file BEFORE imports that need them
load_dotenv()

from flask import Flask, flash, redirect, render_template, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms import FloatField, IntegerField, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from database import init_db as initialize_database
from database import reset_sample_data

from google_reviews import get_google_reviews
from sample_data import GOOGLE_PLACE_ID

# Debug print
print(f"DEBUG - GOOGLE_PLACE_ID from env: {os.getenv('GOOGLE_PLACE_ID')}")
print(f"DEBUG - GOOGLE_PLACE_ID from sample_data: {GOOGLE_PLACE_ID}")

app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "your-secret-key-change-this-in-production"
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///portfolio.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Production settings
if os.getenv("FLASK_ENV") == "production":
    app.config["DEBUG"] = False
    app.config["TESTING"] = False
else:
    app.config["DEBUG"] = True

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Models
class User(UserMixin, db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Lawyer(db.Model):
    """
    Lawyer model - represents the single lawyer profile.
    Note: There will always be only one lawyer record in the system.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    profile_image = db.Column(db.String(200), default="default-lawyer.jpg")

    @staticmethod
    def get_lawyer():
        """Helper method to get the single lawyer record."""
        return db.session.scalars(db.select(Lawyer).limit(1)).first()


class Service(db.Model):
    """Service model - represents legal services offered."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default="fas fa-gavel")


class About(db.Model):
    """About model - represents about us items."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default="fas fa-info-circle")


class Review(db.Model):
    """Review model - represents client reviews (manual/fake ones)."""

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(20), default="manual")  # 'manual' or 'google'

    @staticmethod
    def get_combined_reviews(limit=None):
        """Get combined manual and Google reviews"""
        # Get manual reviews from database
        manual_reviews = db.session.scalars(
            db.select(Review).filter_by(source="manual").order_by(Review.date_created.desc())
        ).all()

        # Get Google reviews
        try:
            google_reviews = get_google_reviews(GOOGLE_PLACE_ID)
        except Exception as e:
            print(f"⚠️  Error fetching Google reviews: {e}")
            google_reviews = []

        # Convert manual reviews to dict format
        manual_reviews_dict = []
        for review in manual_reviews:
            manual_reviews_dict.append(
                {
                    "id": review.id,
                    "client_name": review.client_name,
                    "rating": review.rating,
                    "comment": review.comment,
                    "date_created": review.date_created,
                    "source": "manual",
                    "relative_time": None,
                    "profile_photo": None,
                }
            )

        # Combine and sort by date
        all_reviews = manual_reviews_dict + google_reviews
        all_reviews.sort(
            key=lambda x: x.get("date_created", datetime.now()), reverse=True
        )

        if limit:
            all_reviews = all_reviews[:limit]

        return all_reviews


# Forms
class LawyerForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=2, max=100)])
    title = StringField(
        "Título/Especialização", validators=[DataRequired(), Length(min=2, max=200)]
    )
    description = TextAreaField("Descrição", validators=[DataRequired()])
    phone = StringField("Telefone", validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    address = StringField(
        "Endereço", validators=[DataRequired(), Length(min=10, max=200)]
    )
    lat = FloatField("Latitude", validators=[DataRequired()])
    lng = FloatField("Longitude", validators=[DataRequired()])


class ServiceForm(FlaskForm):
    title = StringField(
        "Título do Serviço", validators=[DataRequired(), Length(min=2, max=100)]
    )
    description = TextAreaField("Descrição", validators=[DataRequired()])
    icon = StringField("Ícone (classe Font Awesome)", default="fas fa-gavel")


class AboutForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField("Descrição", validators=[DataRequired()])
    icon = StringField("Ícone (classe Font Awesome)", default="fas fa-info-circle")


class ReviewForm(FlaskForm):
    client_name = StringField(
        "Nome do Cliente", validators=[DataRequired(), Length(min=2, max=100)]
    )
    rating = IntegerField("Avaliação (1-5)", validators=[DataRequired()])
    comment = TextAreaField("Comentário", validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])


# Routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalars(db.select(User).filter_by(username=form.username.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('admin')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page)
        else:
            flash('Usuário ou senha inválidos!', 'error')
    
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for("index"))


@app.route("/")
def index():
    # Get the single lawyer record
    lawyer = Lawyer.get_lawyer()
    services = db.session.scalars(db.select(Service)).all()
    abouts = db.session.scalars(db.select(About)).all()

    # Get combined reviews (Google + manual)
    reviews = Review.get_combined_reviews(limit=6)

    # Cache busting for CSS - force reload
    import time

    cache_version = int(time.time())

    return render_template(
        "index.html",
        lawyer=lawyer,
        services=services,
        abouts=abouts,
        reviews=reviews,
        cache_version=cache_version,
    )


@app.route("/admin")
@login_required
def admin():
    # Get the single lawyer record
    lawyer = Lawyer.get_lawyer()
    services = db.session.scalars(db.select(Service)).all()
    abouts = db.session.scalars(db.select(About)).all()
    # Get all manual reviews for admin
    manual_reviews = db.session.scalars(
        db.select(Review).filter_by(source="manual")
    ).all()
    # Get Google reviews count
    try:
        google_reviews = get_google_reviews(GOOGLE_PLACE_ID)
        google_count = len(google_reviews)
    except:
        google_count = 0

    # Cache busting for CSS
    import time

    cache_version = int(time.time())

    return render_template(
        "admin.html",
        lawyer=lawyer,
        services=services,
        abouts=abouts,
        reviews=manual_reviews,
        google_reviews_count=google_count,
        cache_version=cache_version,
    )


@app.route("/admin/lawyer", methods=["GET", "POST"])
@login_required
def admin_lawyer():
    # Get the single lawyer record (or None if doesn't exist)
    lawyer = Lawyer.get_lawyer()
    form = LawyerForm()

    if form.validate_on_submit():
        if lawyer:
            # Update existing lawyer record
            lawyer.name = form.name.data
            lawyer.title = form.title.data
            lawyer.description = form.description.data
            lawyer.phone = form.phone.data
            lawyer.email = form.email.data
            lawyer.address = form.address.data
            lawyer.lat = form.lat.data
            lawyer.lng = form.lng.data
        else:
            # Create new lawyer record (should only happen on first setup)
            lawyer = Lawyer(
                name=form.name.data,
                title=form.title.data,
                description=form.description.data,
                phone=form.phone.data,
                email=form.email.data,
                address=form.address.data,
                lat=form.lat.data,
                lng=form.lng.data,
            )
            db.session.add(lawyer)

        db.session.commit()
        flash("Informações atualizadas com sucesso!", "success")
        return redirect(url_for("admin"))

    # Populate form with existing data for GET request
    if lawyer:
        form.name.data = lawyer.name
        form.title.data = lawyer.title
        form.description.data = lawyer.description
        form.phone.data = lawyer.phone
        form.email.data = lawyer.email
        form.address.data = lawyer.address
        form.lat.data = lawyer.lat
        form.lng.data = lawyer.lng

    return render_template("admin_lawyer.html", form=form, lawyer=lawyer)


@app.route("/admin/services", methods=["GET", "POST"])
@login_required
def admin_services():
    form = ServiceForm()

    if form.validate_on_submit():
        service = Service(
            title=form.title.data,
            description=form.description.data,
            icon=form.icon.data,
        )
        db.session.add(service)
        db.session.commit()
        flash("Serviço adicionado com sucesso!", "success")
        return redirect(url_for("admin_services"))

    services = db.session.scalars(db.select(Service)).all()
    return render_template("admin_services.html", form=form, services=services)


@app.route("/admin/services/delete/<int:id>")
@login_required
def delete_service(id):
    service = db.session.get(Service, id)
    if not service:
        abort(404)
    db.session.delete(service)
    db.session.commit()
    flash("Serviço removido com sucesso!", "success")
    return redirect(url_for("admin_services"))


@app.route("/admin/about", methods=["GET", "POST"])
@login_required
def admin_about():
    form = AboutForm()

    if form.validate_on_submit():
        about = About(
            title=form.title.data,
            description=form.description.data,
            icon=form.icon.data,
        )
        db.session.add(about)
        db.session.commit()
        flash("Sobre Nós adicionado com sucesso!", "success")
        return redirect(url_for("admin_about"))

    abouts = db.session.scalars(db.select(About)).all()
    return render_template("admin_about.html", form=form, abouts=abouts)


@app.route("/admin/about/delete/<int:id>")
@login_required
def delete_about(id):
    about = db.session.get(About, id)
    if not about:
        abort(404)
    db.session.delete(about)
    db.session.commit()
    flash("Sobre Nós removido com sucesso!", "success")
    return redirect(url_for("admin_about"))


@app.route("/admin/reviews", methods=["GET", "POST"])
@login_required
def admin_reviews():
    form = ReviewForm()

    if form.validate_on_submit():
        review = Review(
            client_name=form.client_name.data,
            rating=form.rating.data,
            comment=form.comment.data,
            source="manual",  # Mark as manual review
        )
        db.session.add(review)
        db.session.commit()
        flash("Avaliação manual adicionada com sucesso!", "success")
        return redirect(url_for("admin_reviews"))

    # Get manual reviews only (Google reviews are read-only)
    manual_reviews = db.session.scalars(
        db.select(Review).filter_by(source="manual").order_by(Review.date_created.desc())
    ).all()

    # Get Google reviews for display (read-only)
    try:
        google_reviews = get_google_reviews(GOOGLE_PLACE_ID)
    except:
        google_reviews = []

    return render_template(
        "admin_reviews.html",
        form=form,
        manual_reviews=manual_reviews,
        google_reviews=google_reviews,
    )


@app.route("/admin/reviews/delete/<int:id>")
@login_required
def delete_review(id):
    review = db.session.get(Review, id)
    if not review:
        abort(404)
    if review.source == "manual":  # Only allow deleting manual reviews
        db.session.delete(review)
        db.session.commit()
        flash("Avaliação removida com sucesso!", "success")
    else:
        flash("Não é possível remover avaliações do Google!", "error")
    return redirect(url_for("admin_reviews"))


@app.route("/admin/reviews/refresh-google", methods=["POST"])
@login_required
def refresh_google_reviews():
    """Refresh Google reviews (useful for testing)"""
    try:
        google_reviews = get_google_reviews(GOOGLE_PLACE_ID)
        flash(f"✅ {len(google_reviews)} avaliações do Google carregadas!", "success")
    except Exception as e:
        flash(f"❌ Erro ao carregar avaliações do Google: {str(e)}", "error")
    return redirect(url_for("admin_reviews"))


@app.route("/admin/reset-data", methods=["POST"])
@login_required
def admin_reset_data():
    """Reset database to original sample data (useful for development)."""
    try:
        reset_sample_data(db, Lawyer, Service, About, Review, User)
        flash("Banco de dados resetado para dados de exemplo!", "success")
    except Exception as e:
        flash(f"Erro ao resetar dados: {str(e)}", "error")
    return redirect(url_for("admin"))

# Initialize database for all environments (including Vercel)
with app.app_context():
    try:
        # Initialize database using the new separated structure
        initialize_database(db, Lawyer, Service, About, Review, User)
    except Exception as e:
        print(f"Database initialization error: {e}")
        
if __name__ == "__main__":
    # Production vs Development configuration
    if os.getenv("FLASK_ENV") == "production":
        # Production settings
        app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)
    else:
        # Development settings
        app.run(debug=True, port=3000)
