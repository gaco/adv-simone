# database.py
# Database initialization and sample data management

from sample_data import ABOUT_DATA, LAWYER_DATA, SERVICES_DATA


def init_db(db, Lawyer, Service, About, Review):
    """Initialize database with tables and sample data if needed."""

    # Create all tables
    db.create_all()

    # Check if lawyer already exists (there should only be one)
    lawyer = Lawyer.query.first()

    if not lawyer:
        print("Initializing database with sample data...")

        # Create the single lawyer record
        lawyer = Lawyer(**LAWYER_DATA)
        db.session.add(lawyer)

        # Add sample services
        for service_data in SERVICES_DATA:
            service = Service(**service_data)
            db.session.add(service)

        # Add sample about items
        for about_data in ABOUT_DATA:
            about = About(**about_data)
            db.session.add(about)

        # Note: No sample reviews - they should only be added through admin panel

        # Commit all changes
        db.session.commit()
        print("✅ Sample data loaded successfully!")
        print(
            f"📋 Created: 1 lawyer, {len(SERVICES_DATA)} services, {len(ABOUT_DATA)} about items, 0 reviews"
        )
    else:
        print("📊 Database already initialized")


def reset_sample_data(db, Lawyer, Service, About, Review):
    """Reset database to original sample data (useful for development/testing)."""

    print("🔄 Resetting database to sample data...")

    # Clear existing data
    Review.query.delete()
    About.query.delete()
    Service.query.delete()
    Lawyer.query.delete()

    # Re-add sample data
    lawyer = Lawyer(**LAWYER_DATA)
    db.session.add(lawyer)

    for service_data in SERVICES_DATA:
        service = Service(**service_data)
        db.session.add(service)

    for about_data in ABOUT_DATA:
        about = About(**about_data)
        db.session.add(about)

    # Note: No sample reviews - they should only be added through admin panel

    db.session.commit()
    print("✅ Database reset to sample data!")
