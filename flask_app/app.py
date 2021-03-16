#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from forms import *
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import func
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
db = SQLAlchemy(app)
moment = Moment(app)
app.config.from_object('config')
migrate = Migrate(app, db)

class c(db.Model):
    __tablename__ = 'c'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    reg_num = db.Column(db.String(120))
    address1 = db.Column(db.String(120))
    city1 = db.Column(db.String(120))
    county1 = db.Column(db.String(120))
    postcode1 = db.Column(db.String(120))
    address2 = db.Column(db.String(120))
    city2 = db.Column(db.String(120))
    county2 = db.Column(db.String(120))
    postcode2 = db.Column(db.String(120))
    address3 = db.Column(db.String(120))
    city3 = db.Column(db.String(120))
    county3 = db.Column(db.String(120))
    postcode3 = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    linkedin_link = db.Column(db.String(120))
    website = db.Column(db.String(120))

    def __repr__(self):
        return '<Charity {}>'.format(self.name)

class m(db.Model):
    __tablename__ = 'm'

    id = db.Column(db.Integer, primary_key=True)
    waste_stream = db.Column(db.String)
    amount = db.Column(db.Integer)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    county = db.Column(db.String(120))
    condition = db.Column(db.String(120))
    dimensions = db.Column(db.String(120))
    condition = db.Column(db.String(120))
    image_link1 = db.Column(db.String(120))
    image_link2 = db.Column(db.String(120))
    image_link3 = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Material {}>'.format(self.name)


#class request(db.Model):
    #__tablename__ = 'request'
    #id = db.Column(db.Integer, primary_key=True)
    #mat_id = db.Column(db.Integer, nullable=False)
    #e_id = db.Column(db.String(120), nullable=False)
    #message = db.Column(db.String(120))

    #def __repr__(self):
        #return '<Request {}{}>'.format(self.artist_id, self.venue_id)
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/map')
def map():
    return render_template('pages/map.html')

@app.route('/')
def index():
    return render_template('pages/login.html')

@app.route('/home')
def home():
    return render_template('pages/home.html')

#  Create Account
#  ----------------------------------------------------------------

@app.route('/submit_details', methods=['GET'])

def create_account_form():
    form = CharityForm()
    return render_template('forms/new_account.html', form=form)

@app.route('/submit_details', methods=['POST'])

def create_account_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    error=False
    try:
        name = request.form['name']
        email = request.form['email']
        reg_num = request.form['reg_num']
        address1 = request.form['address1']
        city1 = request.form['city1']
        county1 = request.form['county1']
        postcode1 = request.form['postcode1']
        address2 = request.form['address2']
        city2 = request.form['city2']
        county2 = request.form['county2']
        postcode2 = request.form['postcode2']
        address3 = request.form['address3']
        city3 = request.form['city3']
        county3 = request.form['county3']
        postcode3 = request.form['postcode3']
        phone = request.form['phone']
        facebook_link = request.form['facebook_link']
        website = request.form['website']

        charity = c(name=name, email=email, reg_num=reg_num, address1=address1, city1=city1, county1=county1, postcode1=postcode1, address2=address2, city2=city2, 
                    county2=county2, postcode2=postcode2, address3=address3, city3=city3, county3=county3, postcode3=postcode3, phone=phone, 
                    facebook_link=facebook_link, website=website)
        
        db.session.add(charity)
        db.session.commit()
    
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    
    if error:
        flash('Error. Account was not uploaded.')

    if not error:
        flash('Account was successfully uploaded.')
        
    return render_template('pages/home.html')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/



#----------------------------------------------------------------------------#
# Materials Dashboard
#----------------------------------------------------------------------------#
@app.route('/material_input', methods=['GET'])

def create_material_form():
    form = MaterialForm()
    return render_template('forms/new_material.html', form=form)

@app.route('/material_input', methods=['POST'])
def create_material_submission():

    error=False
    try:
        waste_stream = request.form['waste_stream']
        amount = request.form['amount']
        address = request.form['address']
        city = request.form['city']
        county = request.form['county']
        dimensions = request.form['dimensions']
        condition = request.form['condition']
        image_link1 = request.form['image_link1']
        image_link2 = request.form['image_link2']
        image_link3 = request.form['image_link3']

        charity = m(waste_stream=waste_stream, amount=amount, address=address, city=city, county=county, dimensions=dimensions, condition=condition, 
                    image_link1=image_link1, image_link2=image_link2, image_link3=image_link3)
        
        db.session.add(charity)
        db.session.commit()
    
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    
    if error:
        flash('Error. Material was not uploaded.')

    if not error:
        flash('Material was successfully uploaded.')
        
    return render_template('pages/home.html')
  

@app.route('/materials')
def materials():
  # TODO: replace with real materials data.
  # num_shows should be aggregated based on number of upcoming shows per material.
    
    all_areas = m.query.with_entities(func.count(m.id), m.city, m.county).group_by(m.city, m.county).all()
    data = []

    for area in all_areas:
        area_projects = m.query.filter_by(county=area.county).filter_by(city=area.city).all()
    
        project_data = []
    
        for material in area_projects:
            project_data.append({
                "id": material.id,
                "material": material.waste_stream, 
                })
    
    
        data.append({
            "city": area.city,
            "state": area.county, 
            "materials": project_data
            })

    
    return render_template('pages/materials.html', areas=data)


@app.route('/materials/search', methods=['POST'])
def search_materials():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    search_result = db.session.query(m).filter(m.name.ilike(f'%{search_term}%')).all()
    data = []

    for result in search_result:
        data.append({
            "id": result.id,
            "name": result.waste_stream,
        })
  
    response={
        "count": len(search_result),
        "data": data
    }
  
    return render_template('pages/search_materials.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/materials/<int:material_id>')
def show_material(material_id):
  # shows the material page with the given material_id
  # TODO: replace with real material data from the materials table, using material_id

  
    material = m.query.get(material_id)

    if not material: 
        return render_template('errors/404.html')

    data = {
        "id": material.id,
        "material": material.waste_stream,
        "city": material.city,
        "county": material.county,
        "address": material.address,
        "dimensions": material.dimensions,
        "condition": material.condition,
        "image_link1": material.image_link1,
        "image_link2": material.image_link2,
        "image_link3": material.image_link3
    }

    return render_template('pages/show_material.html', material=data)

#  Create Request
#  ----------------------------------------------------------------
@app.route('/material/<int:mat_id>/request', methods=['GET'])
def create_material_request(mat_id):
    form = RequestForm()
    return render_template('forms/new_request.html', form=form)

@app.route('/material/<int:mat_id>/request', methods=['POST'])
def request_material_form(mat_id):
    error=False
    try:
        mat_id = mat_id
        email = request.form['email']
        message = request.form['message']
        
        request = r(mat_id=mat_id, e_id=e_id, message=message)
        db.session.add(request)
        db.session.commit()
    
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    
    if error:
        flash('Error. Request was not sent.')

    if not error:
        flash('Request sent!')
        
    return render_template('pages/home.html')


#  Error Handling and Initializing
#  ----------------------------------------------------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
