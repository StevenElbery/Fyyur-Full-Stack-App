#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app,config(FLASK)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show_id = db.Column(db.Integer, db.ForeignKey('Show.id'), nullable=False)
    seeking_talent=True
    seeking_description=db.Column(db.String)
    upcoming_shows = db.Column(db.Array())
    past_shows = db.Column(db.Array())
    upcoming_shows_count = db.Column(db.Integer)
    past_shows_count = db.Column(db.Integer)
    website=db.Column(db.string)




    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show_id = db.Column(db.Integer, db.ForeignKey('Show.id'), nullable=False)
    num_upcoming_shows = db.Column(db.Integer)
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)


    def __repr__(self):
      return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.name} {self.facebook_link}>'



# TODO: implement any missing fields, as a database migration using Flask-Migrate

#show_artists = db.Table ('show_artists', 
#db.Column(db.Integer, db.ForeignKey('Show.id'), primary_key=True), 
#db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
#)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(120))
    #artists = db.relationship('Artist', secondary = show_artists, backref = db.backref('shows', lazy=True))

    def __repr__(self):
      return f'<Show {self.id} {self.start_time}>'    


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

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
 # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  data=Venue.query.filter_by(city = Venue.city, state = Venue.state).order_by(Venue.state).all()

  return render_template('pages/venues.html', areas=data, venues=Venue.query.all(), num_shows=Venue.query(show.id).count()
)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  return render_template('pages/search_venues.html', 
  results=Artist.query.filter(name.like('%search_term%')), 
  search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
#    "id": Venue.id,
#   "genres": Venue.genres,
#    "address": Venue.address,
#   "city": Venue.city,
#   "state": Venue.state,
#    "phone": Venue.phone,
#    "website": Venue.website,
#    "facebook_link": Venue.facebook_link,
#    "seeking_talent": Venue.seeking_talent,
#    "image_link": Venue.image_link,
#    "past_shows": Venue.past_shows,
#    "upcoming_shows": Venue.upcoming_shows,
#    "past_shows_count": Venue.query(show.id).count.all(),
#    "upcoming_shows_count": 0,

  data = Venue.query(show.id).count.all()
  return render_template('pages/show_venue.html', 
  venue=Venue.query.filter(venue_id=venue_id).all(), num_show=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])


def create_venue_submission():

 # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
 error = False
 try:
  form = request.get_json()['VenueForm']
  db.session.add(form)
  db.session.commit()
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
 except:
   error = True
   db.session.rollback()
   flash('An error occurred. Venue ' + data.name + ' could not be listed.')
   return render_template('pages/home.html', form=form)
  
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  
  try:
    Venue.query.filter_by(venue_id=venue_id).delete()
    db.session.commit()  
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')
 

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  return render_template('pages/artists.html', 
  artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  return render_template('pages/search_artists.html', 
  results=Artist.query.filter(name.ilike('%search_term%')).all(), 
  search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  return render_template('pages/show_artist.html', 
  artist=Artist.query.filter_by(artist_id = artist_id))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', 
  form=form, artist=Artist.query.filter_by(artist_id = artist_id))

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    Artist.query.filter_by(artist_id=artist_id).update()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id), form=ArtistForm)

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venue.query.filter_by(venue_id=venue.id).all()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  try:
    Venue.query.filter_by(venue_id).update()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()  
  
  return redirect(url_for('show_venue', 
  venue_id=venue_id), form=VenueForm,   
  venue=Venue.query.filter_by(id=venue.id).all())

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = request.get_json()['ArtistForm']()
  error = False
  try:
    db.session.add(form)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  else:
    abort(500)
  return render_template('pages/home.html')

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  return render_template('pages/shows.html', shows=Show.query.all())

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  form = request.get_json()['ShowForm']
  try:
    db.session.add(form)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    error = True
    db.session.rollback()
    flash('An error occurred. The show could not be listed!')
  else:
    abort(500)
  return render_template('pages/home.html', form=form)

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

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

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)      
'''
