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
from project_divert_functions import *
from sqlalchemy import text
import math
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
    type = db.Column(db.String(120))
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
    postcode = db.Column(db.String(120))
    condition = db.Column(db.String(120))
    dimensions = db.Column(db.String(120)) 
    image_link1 = db.Column(db.String(120))
    image_link2 = db.Column(db.String(120))
    image_link3 = db.Column(db.String(120))
    longitude = db.Column(db.Float(5))
    latitude = db.Column(db.Float(5))
    
    def __repr__(self):
        return '<Material {}>'.format(self.name)

class output(db.Model):
    __tablename__ = 'output'

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String(120))
    amount = db.Column(db.String(120))
    unit = db.Column(db.String(120))
    site_address = db.Column(db.String(120))
    traditional_address = db.Column(db.String(120))
    divert_address = db.Column(db.String(120))
    traditional_cost = db.Column(db.String(120))
    divert_cost = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __repr__(self):
        return '<Output {}>'.format(self.name)

class r(db.Model):
    __tablename__ = 'r'
    id = db.Column(db.Integer, primary_key=True)
    mat_id = db.Column(db.Integer, nullable=False)
    e_id = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(120))

    def __repr__(self):
        return '<Request {}{}>'.format(self.mat_id)
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
@app.route('/first', methods=['GET'])
def first_get():
    form = FilterForm()
    return render_template('forms/first.html', form=form)

@app.route('/first', methods=['POST'])
def first_post():

    radius = request.form['radius']
    postcode = request.form['postcode']

    endpoint = "http://api.postcodes.io/postcodes/{}".format(postcode)
    r = requests.get(endpoint)
    r = r.text
    y = json.loads(r) 
    target_long = (y.get('result')).get('longitude')
    target_lat = (y.get('result')).get('latitude')
    lat_radians = math.radians(target_lat)
    long_radians = math.radians(target_long)

    all_areas = m.query.filter(func.acos(func.sin(func.radians(target_lat)) * func.sin(func.radians(m.latitude)) + func.cos(func.radians(target_lat)) * func.cos(func.radians(m.latitude)) * func.cos(func.radians(m.longitude) - (func.radians(target_long)))) * 6371 <= 100)
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

@app.route('/map')
def map():
    return render_template('pages/map.html')

@app.route('/')
def index():
    return render_template('pages/login.html')

@app.route('/home')
def home():
    return render_template('pages/home.html')

@app.route('/output', methods=['GET'])
def create_output_form():
    form = OutputForm()
    return render_template('forms/calculator.html', form=form)

@app.route('/output', methods=['POST'])
def create_output_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    error=False
    try:
        material = request.form['material']
        amount = request.form['amount']
        unit = request.form['unit']
        site_address = request.form['site_address']
        traditional_address = request.form['traditional_address']
        divert_address = request.form['divert_address']
        traditional_cost= request.form['traditional_cost']
        divert_cost = request.form['divert_cost']

        g = output(material=material, amount=amount, unit=unit, site_address=site_address, traditional_address=traditional_address, 
                        divert_address=divert_address, traditional_cost=traditional_cost, divert_cost=divert_cost)
        db.session.add(g)
        db.session.commit()
    
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())

    finally:
        db.session.close()
    
    if error:
        flash('An error occurred. Output for ' + request.form['material']+ ' could not be calculated.')

    if not error:
        flash('Output for ' + request.form['material'] + ' was successfully listed.')
    
    return redirect("/result")

def fun(material, amount, unit, site_address, traditional_address, divert_address, traditional_cost):
    
    if material == 'carpet tiles':
        if unit == 'Square Meters':
            amount=(amount*4.3)/1000

    mrf_transport_carbon  = numeric_distance(traditional_address, site_address) * 0.85
    landfill_transport_carbon = mrf_transport_carbon * 1.2
    landfill_monetary_cost = traditional_cost + 114
    mrf_to_reprocessor_cost = traditional_cost
    mrf_to_reprocessor_transport_carbon = mrf_transport_carbon * 1.2
    divert_transport_carbon  = numeric_distance(divert_address, site_address) * 0.85

    g=reuse_offset.index
    g=g.to_list()
    error=False
    
    if material in g:
        reuse_embodied_carbon = amount * reuse_offset.loc[f'{material}', 'Emission Factor (kg CO2 equivalents/ tonne)']
    else:
        error=True
        print('Error!')
        
    g=recycle_offset.index
    g=g.to_list()
    
    if material in g:
        recycle_embodied_carbon = amount * recycle_offset.loc[f'{material}', 'Emission Factor (kg CO2 equivalents/ tonne or sq m)']
    
    else:
        recycle_embodied_carbon = (amount * reuse_offset.loc[f'{material}', 'Emission Factor (kg CO2 equivalents/ tonne)'])*0.85
        
    return mrf_transport_carbon, landfill_transport_carbon, landfill_monetary_cost, mrf_to_reprocessor_cost, mrf_to_reprocessor_transport_carbon, divert_transport_carbon, reuse_embodied_carbon, recycle_embodied_carbon


@app.route('/result')
def show_output():
  output_query = db.session.query(output).order_by(output.id.desc()).first()
  

  if not output_query: 
    return render_template('errors/404.html')


  g = fun(output_query.material, float(output_query.amount), output_query.unit, output_query.site_address, output_query.traditional_address, output_query.divert_address, float(output_query.traditional_cost))
  
  mrf_transport_carbon = g[0]
  landfill_transport_carbon = g[1]
  landfill_monetary_cost = g[2]
  mrf_to_reprocessor_cost = g[3]
  mrf_to_reprocessor_transport_carbon = g[4]
  divert_transport_carbon = g[5]
  reuse_embodied_carbon = g[6]
  recycle_embodied_carbon = g[7]

  

  data = {
    "mrf_transport_carbon": mrf_transport_carbon,
    "landfill_transport_carbon": landfill_transport_carbon,
    "landfill_monetary_cost": landfill_monetary_cost,
    "mrf_to_reprocessor_cost": mrf_to_reprocessor_cost,
    "mrf_to_reprocessor_transport_carbon": mrf_to_reprocessor_transport_carbon,
    "mrf_to_reprocessor_embodied_carbon": (recycle_embodied_carbon * 0.7),
    "divert_transport_carbon": divert_transport_carbon,
    "reuse_embodied_carbon": reuse_embodied_carbon,
    "recycle_embodied_carbon": recycle_embodied_carbon,
    "divert_cost": output_query.divert_cost,
    "traditional_cost": output_query.traditional_cost,
    "traditional_carbon": (mrf_transport_carbon - (recycle_embodied_carbon * 0.7)),
    "divert_recycle_total_carbon": (-recycle_embodied_carbon + divert_transport_carbon),
    "divert_reuse_total_carbon": (-reuse_embodied_carbon + divert_transport_carbon),
    "mrf_to_reprocessor_carbon": (mrf_to_reprocessor_transport_carbon - (recycle_embodied_carbon * 0.7))
  }

  return render_template('pages/output.html', output=data)
#  Create Account
#  ----------------------------------------------------------------

@app.route('/submit_details1', methods=['GET'])
def create_account_form1():
    form = CharityForm1()
    return render_template('forms/new_account.html', form=form)

@app.route('/submit_details1', methods=['POST'])
def create_account_submission1():

    error=False
    try:
        name = request.form['name']
        type = 'Charity'
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

        charity = c(name=name, type=type, email=email, reg_num=reg_num, address1=address1, city1=city1, county1=county1, postcode1=postcode1, address2=address2, city2=city2, 
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
        
    return redirect('/first')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/submit_details2', methods=['GET'])
def create_account_form2():
    form = CharityForm2()
    return render_template('forms/new_account.html', form=form)

@app.route('/submit_details2', methods=['POST'])
def create_account_submission2():

    error=False
    try:
        name = request.form['name']
        type = 'Community Group'
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

        charity = c(name=name, type=type, email=email, reg_num=reg_num, address1=address1, city1=city1, county1=county1, postcode1=postcode1, address2=address2, city2=city2, 
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
        
    return redirect('/first')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/submit_details3', methods=['GET'])
def create_account_form3():
    form = CharityForm3()
    return render_template('forms/new_account.html', form=form)

@app.route('/submit_details3', methods=['POST'])
def create_account_submission3():

    error=False
    try:
        name = request.form['name']
        type = 'Education'
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

        charity = c(name=name, type=type, email=email, reg_num=reg_num, address1=address1, city1=city1, county1=county1, postcode1=postcode1, address2=address2, city2=city2, 
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
        
    return redirect('/first')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/submit_details4', methods=['GET'])
def create_account_form4():
    form = CharityForm4()
    return render_template('forms/new_account.html', form=form)

@app.route('/submit_details4', methods=['POST'])
def create_account_submission4():

    error=False
    try:
        name = request.form['name']
        type = 'Social Enterprise'
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

        charity = c(name=name, type=type, email=email, reg_num=reg_num, address1=address1, city1=city1, county1=county1, postcode1=postcode1, address2=address2, city2=city2, 
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
        
    return redirect('/first')
  
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/submit_details5', methods=['GET'])
def create_account_form5():
    form = CharityForm5()
    return render_template('forms/new_account_other.html', form=form)

@app.route('/submit_details5', methods=['POST'])
def create_account_submission5():

    error=False
    try:
        name = request.form['name']
        type = request.form['other']
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

        charity = c(name=name, type=type, email=email, reg_num=reg_num, address1=address1, city1=city1, county1=county1, postcode1=postcode1, address2=address2, city2=city2, 
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
        
    return redirect('/first')
  
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
        postcode = request.form['postcode']
        endpoint = "http://api.postcodes.io/postcodes/{}".format(postcode)
        r = requests.get(endpoint)
        r = r.text
        y = json.loads(r) 
        longitude = (y.get('result')).get('longitude')
        latitude = (y.get('result')).get('latitude')
        dimensions = request.form['dimensions']
        condition = request.form['condition']
        image_link1 = request.form['image_link1']
        image_link2 = request.form['image_link2']
        image_link3 = request.form['image_link3']


        charity = m(waste_stream=waste_stream, amount=amount, address=address, city=city, county=county, postcode=postcode, dimensions=dimensions, condition=condition, 
                    image_link1=image_link1, image_link2=image_link2, image_link3=image_link3, longitude=longitude, latitude=latitude)
        
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
        
    return redirect('/materials')
  

@app.route('/materials')
def materials():
    
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
            "county": area.county, 
            "materials": project_data
            })

    
    return render_template('pages/materials.html', areas=data)


@app.route('/materials/search', methods=['POST'])
def search_materials():

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
  
    material = m.query.get(material_id)

    if not material: 
        return render_template('errors/404.html')

    data = {
        "id": material.id,
        "material": material.waste_stream,
        "amount": material.amount,
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


@app.route('/materials_filtered/<string:location_id>')
def show_site_material(location_id):
    all_areas = m.query.filter(m.city == location_id)
    all_areas = m.query.with_entities(func.count(m.id), m.city, m.county).group_by(m.city, m.county).all()
    data = []

    for area in all_areas:
        if area.city == location_id:
            area_projects = m.query.filter_by(county=area.county).filter_by(city=area.city).all()
        
            project_data = []
        
            for material in area_projects:
                project_data.append({
                    "id": material.id,
                    "material": material.waste_stream, 
                    })
        
        
            data.append({
                "city": area.city,
                "county": area.county, 
                "materials": project_data
                })

    
    return render_template('pages/materials.html', areas=data)

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
        
        qui = r(mat_id=mat_id, e_id=email, message=message)
        db.session.add(qui)
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
        
    return redirect('/materials')

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
