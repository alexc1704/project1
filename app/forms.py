from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length


class PropertyForm(FlaskForm):
    title = StringField(
        'Property Title',
        validators=[DataRequired(), Length(max=255)]
    )
    description = TextAreaField(
        'Description',
        validators=[DataRequired()]
    )
    no_of_rooms = IntegerField(
        'No. of Rooms',
        validators=[DataRequired(), NumberRange(min=1)]
    )
    no_of_bathrooms = IntegerField(
        'No. of Bathrooms',
        validators=[DataRequired(), NumberRange(min=1)]
    )
    price = DecimalField(
        'Price',
        places=2,
        validators=[DataRequired(), NumberRange(min=0)]
    )
    property_type = SelectField(
        'Property Type',
        choices=[('House', 'House'), ('Apartment', 'Apartment')],
        validators=[DataRequired()]
    )
    location = StringField(
        'Location',
        validators=[DataRequired(), Length(max=255)]
    )
    photo = FileField(
        'Photo',
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
        ]
    )
