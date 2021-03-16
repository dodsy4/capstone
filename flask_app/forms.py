from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, FileField, SelectMultipleField, DateTimeField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL

class CharityForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    reg_num = StringField(
        'reg_num'
    )
    email = StringField(
        'email', validators=[DataRequired()]
    )
    city1 = StringField(
        'city1', validators=[DataRequired()]
    )
    city2 = StringField(
        'city2'
    )
    city3 = StringField(
        'city3'
    )

    address1 = StringField(
        # TODO implement validation logic for state
        'address1', validators=[DataRequired()]
    )

    address2 = StringField(
        # TODO implement validation logic for state
        'address2'
    )
    address3 = StringField(
        # TODO implement validation logic for state
        'address3'
    )
    postcode1 = StringField(
        # TODO implement validation logic for state
        'postcode1', validators=[DataRequired()]
    )
    postcode2 = StringField(
        # TODO implement validation logic for state
        'postcode2'
    )
    postcode3 = StringField(
        # TODO implement validation logic for state
        'postcode3'
    )
    county1 = SelectField(
        'county1', validators=[DataRequired()],
        choices=[

            'Bath and North East Somerset',
            'Bedfordshire',
            'Berkshire',
            'Bristol',
            'Buckinghamshire',
            'Cambridgeshire',
            'Cheshire',
            'Cornwall',
            'County Durham',
            'Cumbria',
            'Derbyshire',
            'Devon',
            'Dorset',
            'East Riding of Yorkshire',
            'East Sussex',
            'Essex',
            'Gloucestershire',
            'Greater London',
            'Greater Manchester',
            'Hampshire',
            'Herefordshire',
            'Hertfordshire',
            'Isle of Wight',
            'Isles of Scilly',
            'Kent',
            'Lancashire',
            'Leicestershire',
            'Lincolnshire',
            'Merseyside',
            'Norfolk',
            'North Somerset',
            'North Yorkshire',
            'Northamptonshire',
            'Northumberland',
            'Nottinghamshire',
            'Oxfordshire',
            'Rutland',
            'Shropshire',
            'Somerset',
            'South Gloucestershire',
            'South Yorkshire',
            'Staffordshire',
            'Suffolk',
            'Surrey',
            'Tyne & Wear',
            'Warwickshire',
            'West Midlands',
            'West Sussex',
            'West Yorkshire',
            'Wiltshire',
            'Worcestershire',
            ]
        )
    county2 = SelectField(
        'county2', validators=[DataRequired()],
        choices=[

            'Bath and North East Somerset',
            'Bedfordshire',
            'Berkshire',
            'Bristol',
            'Buckinghamshire',
            'Cambridgeshire',
            'Cheshire',
            'Cornwall',
            'County Durham',
            'Cumbria',
            'Derbyshire',
            'Devon',
            'Dorset',
            'East Riding of Yorkshire',
            'East Sussex',
            'Essex',
            'Gloucestershire',
            'Greater London',
            'Greater Manchester',
            'Hampshire',
            'Herefordshire',
            'Hertfordshire',
            'Isle of Wight',
            'Isles of Scilly',
            'Kent',
            'Lancashire',
            'Leicestershire',
            'Lincolnshire',
            'Merseyside',
            'Norfolk',
            'North Somerset',
            'North Yorkshire',
            'Northamptonshire',
            'Northumberland',
            'Nottinghamshire',
            'Oxfordshire',
            'Rutland',
            'Shropshire',
            'Somerset',
            'South Gloucestershire',
            'South Yorkshire',
            'Staffordshire',
            'Suffolk',
            'Surrey',
            'Tyne & Wear',
            'Warwickshire',
            'West Midlands',
            'West Sussex',
            'West Yorkshire',
            'Wiltshire',
            'Worcestershire',
            ]
        )
    county3 = SelectField(
        'county3', validators=[DataRequired()],
        choices=[

            'Bath and North East Somerset',
            'Bedfordshire',
            'Berkshire',
            'Bristol',
            'Buckinghamshire',
            'Cambridgeshire',
            'Cheshire',
            'Cornwall',
            'County Durham',
            'Cumbria',
            'Derbyshire',
            'Devon',
            'Dorset',
            'East Riding of Yorkshire',
            'East Sussex',
            'Essex',
            'Gloucestershire',
            'Greater London',
            'Greater Manchester',
            'Hampshire',
            'Herefordshire',
            'Hertfordshire',
            'Isle of Wight',
            'Isles of Scilly',
            'Kent',
            'Lancashire',
            'Leicestershire',
            'Lincolnshire',
            'Merseyside',
            'Norfolk',
            'North Somerset',
            'North Yorkshire',
            'Northamptonshire',
            'Northumberland',
            'Nottinghamshire',
            'Oxfordshire',
            'Rutland',
            'Shropshire',
            'Somerset',
            'South Gloucestershire',
            'South Yorkshire',
            'Staffordshire',
            'Suffolk',
            'Surrey',
            'Tyne & Wear',
            'Warwickshire',
            'West Midlands',
            'West Sussex',
            'West Yorkshire',
            'Wiltshire',
            'Worcestershire',
            ]
        )
    phone = StringField(
        'phone'
    )

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    linkedin_link = StringField(
        'linkedin_link', validators=[URL()]
    )

    website= StringField(
        'website', validators=[URL()]
    )

class MaterialForm(FlaskForm):
    waste_stream = SelectField(
        'waste_stream', validators=[DataRequired()],
        choices=[
            'AC Unit',
            'Carpet Tiles',
            'Chair',
            'Desk',
            'Electric Heater',
            'Glass',
            'Lockers',
            'Paving Slabs',
            'Pedestals',
            'Rock/Boulders',
            'Power Sockets',
            'Sand',
            'Shelving'
            'Task Chair',
            'Whiteboard']
    )

    amount = FloatField(
        'amount', validators=[DataRequired()]
    )

    address = StringField(

        'address', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )
    county = SelectField(
        'county', validators=[DataRequired()],
        choices=[

            'Bath and North East Somerset',
            'Bedfordshire',
            'Berkshire',
            'Bristol',
            'Buckinghamshire',
            'Cambridgeshire',
            'Cheshire',
            'Cornwall',
            'County Durham',
            'Cumbria',
            'Derbyshire',
            'Devon',
            'Dorset',
            'East Riding of Yorkshire',
            'East Sussex',
            'Essex',
            'Gloucestershire',
            'Greater London',
            'Greater Manchester',
            'Hampshire',
            'Herefordshire',
            'Hertfordshire',
            'Isle of Wight',
            'Isles of Scilly',
            'Kent',
            'Lancashire',
            'Leicestershire',
            'Lincolnshire',
            'Merseyside',
            'Norfolk',
            'North Somerset',
            'North Yorkshire',
            'Northamptonshire',
            'Northumberland',
            'Nottinghamshire',
            'Oxfordshire',
            'Rutland',
            'Shropshire',
            'Somerset',
            'South Gloucestershire',
            'South Yorkshire',
            'Staffordshire',
            'Suffolk',
            'Surrey',
            'Tyne & Wear',
            'Warwickshire',
            'West Midlands',
            'West Sussex',
            'West Yorkshire',
            'Wiltshire',
            'Worcestershire',
            ]
        )
    dimensions = StringField(
        'dimensions'
    )

    condition = TextAreaField(
        'condition'
    )

    image_link1 = StringField(
        'image_link1'
    )

    image_link2 = StringField(
        'image_link2'
    )

    image_link3 = StringField(
        'image_link3'
    )


class RequestForm(FlaskForm):
    email = StringField(
        'email', validators=[DataRequired()]
    )
    message = TextAreaField(
        'message', validators=[DataRequired()]
    )

