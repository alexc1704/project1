import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory, current_app
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import Property
from app.forms import PropertyForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()

    if form.validate_on_submit():
        # Handle file upload
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        # Prepend a UUID to avoid name collisions
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        photo.save(os.path.join(upload_folder, unique_filename))

        # Save to database
        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            no_of_rooms=form.no_of_rooms.data,
            no_of_bathrooms=form.no_of_bathrooms.data,
            price=form.price.data,
            property_type=form.property_type.data,
            location=form.location.data,
            photo=unique_filename
        )
        db.session.add(new_property)
        db.session.commit()

        flash('Property successfully added!', 'success')
        return redirect(url_for('main.properties'))

    return render_template('create_property.html', form=form)


@main.route('/properties')
def properties():
    all_properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('properties.html', properties=all_properties)


@main.route('/properties/<int:propertyid>')
def property_detail(propertyid):
    prop = Property.query.get_or_404(propertyid)
    return render_template('property_detail.html', property=prop)


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)