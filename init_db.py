# init_db.py

from app import create_app, db
from app.models import Type, Style


app = create_app()

with app.app_context():
    # Drop all existing tables (optional, only if you want a clean reset)
    db.drop_all()

    # Create all tables based on the models
    db.create_all()

    # Insert default types if they don't already exist
    default_types = ['Tango', 'Vals', 'Milonga']
    for type_name in default_types:
        existing_type = Type.query.filter_by(name=type_name).first()
        if not existing_type:
            new_type = Type(name=type_name)
            db.session.add(new_type)

    # Insert default styles if they don't already exist
    default_styles = ['Rhythmic', 'Melodic', 'Dramatic', 'Other']
    for style_name in default_styles:
        existing_style = Style.query.filter_by(name=style_name).first()
        if not existing_style:
            new_style = Style(name=style_name)
            db.session.add(new_style)

    db.session.commit()

print("Database initialized successfully.")
