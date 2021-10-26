from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sqlalchemy.sql import text
from sqlalchemy import func
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

import models
from errors import bad_request

sentry_sdk.init(
    dsn='https://bbf1e21e7ed04190a0ff5be402ca21b4@o983081.ingest.sentry.io/5938602',
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
swagger = Swagger(app)

@app.route('/')
def hello_world():
    try:
        res = jsonify({
            'message': 'API server up and running.'
        })
        res.headers.add('Access-Control-Allow-Origin', '*')
        res.status_code = 201
        return res
    except Exception as e:
        return bad_request(str(e))

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

@app.route('/artists')
def artist_list():
    """
    Artists endpoint returning a list of artists
    ---
    responses:
        200:
            description: A list of artists
    """
    query = models.Artist.query.all()
    artists = [{'id': artist.artist_id, 'name': artist.artist_name} for artist in query]
    
    return jsonify({'data': artists})
    
@app.route('/artists/<int:artist_id>')
def artist(artist_id):
    Artist = models.Artist
    query = Artist.query.filter(Artist.artist_id == artist_id).one_or_none()
    
    return jsonify({
        'data': {
            'artist': {
                'id': query.artist_id,
                'name': query.artist_name
            }
        },
    })

@app.route('/events')
def event_list():
    Artist = models.Artist
    ArtistGenre = models.ArtistGenre
    Cities = models.Cities
    Events = models.Events
    Event_Artist = models.EventArtist
    Genres = models.Genres
    Metropolitan_Area = models.MetropolitanArea
    Venues = models.Venues
    
    metro_input = request.args.get('metro')
    genre_input = request.args.get('genre')
    response = []
    
    artist_genre_query = None
    cities_query = None
    events_query = None
    genre_query = None
    metro_query = None
    venues_query = None

    if metro_input:
        if "_" in metro_input:
            metro_input = metro_input.replace('_', ' ')
        metro_query = Metropolitan_Area.query.filter(
            func.lower(Metropolitan_Area.metropolitan_name) == metro_input.lower()
        ).one_or_none()
        
        cities_query = Cities.query.filter_by(
            metropolitan_id=metro_query.metropolitan_id
        ).all()
        city_ids = [city.city_id for city in cities_query]

        venues_query = Venues.query.filter(Venues.city_id.in_(city_ids))
        venue_ids = [venue.venue_id for venue in venues_query]
        
        events_query = Events.query.filter(Events.venue_id.in_(venue_ids))
    else:
        events_query = Events.query.all()
        
    if genre_input:
        if '_' in genre_input:
            genre_input = genre_input.replace('_', ' ')
        genre_query = Genres.query.filter(
            func.lower(Genres.genre_name) == genre_input.lower()
        ).one_or_none()
    
    for event in events_query:
        event_artist_query = Event_Artist.query.filter(
            Event_Artist.event_id == event.event_id
        ).one_or_none()
        
        if event_artist_query == None:
            continue
        else:
            genre_names = []
            artist_query = Artist.query.filter(
                Artist.artist_id == event_artist_query.artist_id).one_or_none()
            
            if genre_input and genre_input.lower() == genre_query.genre_name.lower():
                artist_genre_query = ArtistGenre.query\
                    .join(Genres, ArtistGenre.genre_id == Genres.genre_id)\
                    .filter(ArtistGenre.artist_id == artist_query.artist_id,
                        ArtistGenre.genre_id == genre_query.genre_id)
                artist_genre_matches = len([artist_genre for artist_genre in artist_genre_query])
                if artist_genre_matches < 1:
                    continue
                else:
                    genre_names.append(genre_query.genre_name)
            else:
                genre_ids = [item.genre_id for item in artist_genre_query]
                genres_query = Genres.query.filter(
                    Genres.genre_id.in_(genre_ids))
                genre_names = [genre.genre_name for genre in genres_query]
            
                artist_genre_query = ArtistGenre.query\
                    .join(Genres, ArtistGenre.genre_id == Genres.genre_id)\
                    .filter(ArtistGenre.artist_id == artist_query.artist_id)          
            
            if metro_input:  
                venue = [venue for venue in venues_query if venue.venue_id == event.venue_id][0]
            else:
                venue = Venues.query.filter(
                    Venues.venue_id == event.venue_id).one_or_none()
                city_query = Cities.query.filter(
                    Cities.city_id == venue.city_id).one_or_none()
                metro_query = Metropolitan_Area.query.filter(
                    Metropolitan_Area.metropolitan_id == city_query.metropolitan_id).one_or_none()
            
            response.append({
                'id': event.event_id,
                'artist': artist_query.artist_name,
                'date': event.event_date,
                'end_at': str(event.event_end_at),
                'genres': genre_names,
                'name': event.event_name,
                'metro': metro_query.metropolitan_name,
                'start_at': str(event.event_start_at),
                'tickets_url': event.tickets_link,
                'type': event.event_type,
                'venue': {
                    'id': venue.venue_id,
                    'name': venue.venue_name,
                    'address': venue.venue_address,
                },
            })
    return jsonify({'data': response})

@app.route('/events/<int:event_id>')
def event_details(event_id):
    Artist = models.Artist
    Cities = models.Cities
    Events = models.Events
    Event_Artist = models.EventArtist
    Metropolitan_Area = models.MetropolitanArea
    Venues = models.Venues

    event = Events.query.filter(Events.event_id == event_id).one_or_none()
    event_artist_query = Event_Artist.query.filter(
        Event_Artist.event_id == event_id
    ).one_or_none()
    
    artist_query = Artist.query.filter(Artist.artist_id == event_artist_query.artist_id).one_or_none()
    venue = Venues.query.filter(Venues.venue_id == event.venue_id).one_or_none()
    city = Cities.query.filter(Cities.city_id == venue.city_id).one_or_none()
    metropolitan_area = Metropolitan_Area.query.filter(
        Metropolitan_Area.metropolitan_id == city.metropolitan_id
    ).one_or_none()

    return jsonify({
        'event_id': event.event_id,
        'artist': artist_query.artist_name,
        'date': event.event_date,
        'city': {
            'name': city.city_name,
            'state': city.city_state,
        },
        'end_at': str(event.event_end_at),
        'name': event.event_name,
        'metropolitan_area': metropolitan_area.metropolitan_name,
        'start_at': str(event.event_start_at),
        'tickets_url': event.tickets_link,
        'type': event.event_type,
        'venue': {
            'name': venue.venue_name,
            'address': venue.venue_address,
        },
    })
    
@app.route('/event_artists')
def event_artist_list():
    Event_Artist = models.EventArtist
    event_artist_query = Event_Artist.query.all()
    
    event_artists = [{
        'id': event_artist.id,
        'artist_id': event_artist.artist_id,
        'event_id': event_artist.event_id,
        'headliner': event_artist.is_headliner,
    } for event_artist in event_artist_query]
        
    return jsonify({
        'data': event_artists
    })
    
    
@app.route('/genres')
def genre_list():
    Genres = models.Genres
    genre_query = Genres.query.all()
    genres = []

    for genre in genre_query:
        genres.append({
            'id': genre.genre_id,
            'name': genre.genre_name,
        })

    return jsonify({
        'data': genres
    })

    
@app.route('/metropolitans')
def metropolitan_list():
    MetropolitanArea = models.MetropolitanArea
    metro_query = MetropolitanArea.query.all()
    metro_areas = []
    
    for area in metro_query:
        metro_areas.append({
            'id': area.metropolitan_id,
            'name': area.metropolitan_name,
        })
    
    return jsonify({
        'data': metro_areas
    })
    

@app.route('/venues')
def venue_list():
    #Venues.query.filter(Venues.venue_id == event.venue_id).one_or_none()
    return None
