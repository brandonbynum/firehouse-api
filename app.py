# import aiohttp
# import asyncio
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from sqlalchemy.sql import text
import json
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from utilities.timer import Timer 
from utilities.defaultConverters import dateToStringConverter
import models
from errors import bad_request
from api.services.event_services import EventService
# from api.services.songkick_event_service import SongKickEventService

sentry_sdk.init(
    dsn='https://bbf1e21e7ed04190a0ff5be402ca21b4@o983081.ingest.sentry.io/5938602',
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

app = Flask(__name__)
app.config.from_object('config.LocalConfig')
db = SQLAlchemy(app)
swagger = Swagger(app)

Artist = models.Artist
ArtistGenre = models.ArtistGenre
Cities = models.Cities
Events = models.Events
Event_Artist = models.EventArtist
Genres = models.Genres
Metropolitan_Area = models.MetropolitanArea
Venues = models.Venues

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

# @app.route('/artists')
# def artist_list():
#     """
#     Artists endpoint returning a list of artists
#     ---
#     responses:
#         200:
#             description: A list of artists
#     """
#     query = models.Artist.query.all()
#     artists = [{'id': artist.artist_id, 'name': artist.artist_name} for artist in query]
    
#     return jsonify({'data': artists})
    
# @app.route('/artists/<int:artist_id>')
# def artist(artist_id):
#     query = Artist.query.filter(Artist.artist_id == artist_id).one_or_none()
    
#     return jsonify({
#         'data': {
#             'artist': {
#                 'id': query.artist_id,
#                 'name': query.artist_name
#             }
#         },
#     })

@app.route('/events')
def event_list():
    """
    Returns list of upcoming events
    ---
    responses:
        200:
            description: A list of events
    """
    event_service = EventService()
    
    genre_input = request.args.get('genre')
    metro_input = request.args.get('metro')
    
    # TODO: Create helper function to remove "_"??
    if genre_input and '_' in genre_input:
        genre_input = genre_input.replace('_', ' ')
    
    if metro_input and '_' in metro_input:
        metro_input = metro_input.replace('_', ' ')
    
    # TODO: Error handling to return 500 or 400 errors
    res = event_service.upcoming_events_test(genre_input, metro_input)
    json_output = json.dumps(res, indent=4, sort_keys=True, default=dateToStringConverter)
    
    return json_output

# @app.route('/events/<int:event_id>')
# def event_details(event_id):
#     event = Events.query.filter(Events.event_id == event_id).one_or_none()
#     event_artist_query = Event_Artist.query.filter(
#         Event_Artist.event_id == event_id
#     ).one_or_none()
    
#     artist_query = Artist.query.filter(Artist.artist_id == event_artist_query.artist_id).one_or_none()
#     venue = Venues.query.filter(Venues.venue_id == event.venue_id).one_or_none()
#     city = Cities.query.filter(Cities.city_id == venue.city_id).one_or_none()
#     metropolitan_area = Metropolitan_Area.query.filter(
#         Metropolitan_Area.metropolitan_id == city.metropolitan_id
#     ).one_or_none()

#     return jsonify({
#         'event_id': event.event_id,
#         'artist': artist_query.artist_name,
#         'date': event.event_date,
#         'city': {
#             'name': city.city_name,
#             'state': city.city_state,
#         },
#         'end_at': str(event.event_end_at),
#         'name': event.event_name,
#         'metropolitan_area': metropolitan_area.metropolitan_name,
#         'start_at': str(event.event_start_at),
#         'tickets_url': event.tickets_link,
#         'type': event.event_type,
#         'venue': {
#             'name': venue.venue_name,
#             'address': venue.venue_address,
#         },
#     })
    
# @app.route('/events/import/<int:metro_id>')
# def songkick_event_import(metro_id):
#     songkick_service = SongkickEventService()
#     metro = Metropolitan_Area.query.filter_by(
#         metropolitan_id = metro_id
#     ).one_or_none()
    
#     asyncio.run(songkick_service.process_events(metro.metropolitan_name))
    
    
    
# @app.route('/event_artists')
# def event_artist_list():
#     event_artist_query = Event_Artist.query.all()
    
#     event_artists = [{
#         'id': event_artist.id,
#         'artist_id': event_artist.artist_id,
#         'event_id': event_artist.event_id,
#         'headliner': event_artist.is_headliner,
#     } for event_artist in event_artist_query]
        
#     return jsonify({
#         'data': event_artists
#     })
    
    
# @app.route('/genres')
# def genre_list():
#     genre_query = Genres.query.all()
#     genres = []

#     for genre in genre_query:
#         genres.append({
#             'id': genre.genre_id,
#             'name': genre.genre_name,
#         })

#     return jsonify({
#         'data': genres
#     })

    
# @app.route('/metropolitans')
# def metropolitan_list():
#     metro_query = Metropolitan_Area.query.all()
#     metro_areas = []
    
#     for area in metro_query:
#         metro_areas.append({
#             'id': area.metropolitan_id,
#             'name': area.metropolitan_name,
#         })
    
#     return jsonify({
#         'data': metro_areas
#     })
    
# @app.route('/venues')
# def venue_list():
#     #Venues.query.filter(Venues.venue_id == event.venue_id).one_or_none()
#     return None