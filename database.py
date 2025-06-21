# database.py
# Database initialization and sample data management

import os
from sample_data import ABOUT_DATA, LAWYER_DATA, SERVICES_DATA


def init_db(db, Lawyer, Service, About, Review, User):
    """Initialize database with tables and sample data if needed."""

    # Create all tables
    db.create_all()

    # Check if admin user exists, if not create one
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    admin_user = db.session.scalars(db.select(User).filter_by(username=admin_username)).first()
    if not admin_user:
        print("Creating default admin user...")
        admin_user = User(username=admin_username)
        admin_user.set_password(admin_password)
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Default admin user created!")
        print(f"👤 Username: {admin_username}")
        print(f"🔑 Password: {admin_password}")
        print("⚠️  IMPORTANT: Change the default password in production!")

    # Check if lawyer already exists (there should only be one)
    lawyer = db.session.scalars(db.select(Lawyer).limit(1)).first()

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


def reset_sample_data(db, Lawyer, Service, About, Review, User):
    """Reset database to original sample data (useful for development/testing)."""

    print("🔄 Resetting database to sample data...")

    # Clear existing data
    db.session.execute(db.delete(Review))
    db.session.execute(db.delete(About))
    db.session.execute(db.delete(Service))
    db.session.execute(db.delete(Lawyer))
    db.session.execute(db.delete(User))

    # Create admin user with environment variables
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    admin_user = User(username=admin_username)
    admin_user.set_password(admin_password)
    db.session.add(admin_user)

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
    print(f"👤 Admin user: {admin_username} / {admin_password}")
