# import aiohttp
# import asyncio
from flask import Blueprint, Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
import json
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from errors import bad_request
from api.services.event_services import EventService

from models import Artist
from models import ArtistGenre
from models import Cities
from models import Events
from models import EventArtist
from models import Genres
from models import MetropolitanArea
from models import Venues

from utilities.dateTimeEncoder import DateTimeEncoder
from utilities.pretty_print import pretty_print as pp

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
CORS(app, resources={r'/api/*': {'origins': '*'}})
db = SQLAlchemy(app)
swagger = Swagger(app)

ui_api = Blueprint('api', __name__, url_prefix='/api')

@ui_api.route('/')
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

@ui_api.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

@ui_api.route('/artists', methods=['GET'])
def artist_list():
    """
    Artists endpoint returning a list of artists
    ---
    responses:
        200:
            description: A list of artists
    """
    query = Artist.query.all()
    artists = [{'id': artist.id, 'name': artist.name} for artist in query]
    return jsonify({'data': artists})
    
@ui_api.route('/artists/<int:artist_id>', methods=['GET'])
def artist(artist_id):
    query = Artist.query.filter(Artist.id == artist_id).one_or_none()
    
    return jsonify({
        'data': {
            'artist': {
                'id': query.id,
                'name': query.name
            }
        },
    })

@ui_api.route('/events')
def event_list():
    """
    Returns list of upcoming events
    ---
    responses:
        200:
            description: A list of events
    """
    event_service = EventService()
    metro_input = request.args.get('metro')
    
    if metro_input and '_' in metro_input:
        metro_input = metro_input.replace('_', ' ')
    
    # TODO: Error handling to return 500 or 400 errors
    res = event_service.upcoming_events_test(metro_input)
    json_output = json.dumps(res, indent=4, cls=DateTimeEncoder)
    
    return json_output
    

@ui_api.route('/events/<int:event_id>')
def event_details(event_id):
    res = EventService.get_event_details(event_id)
    return jsonify(res)
    
# @app.route('/events/import/<int:metro_id>')
# def songkick_event_import(metro_id):
#     songkick_service = SongkickEventService()
#     metro = Metropolitan_Area.query.filter_by(
#         metropolitan_id = metro_id
#     ).one_or_none()
    
#     asyncio.run(songkick_service.process_events(metro.metropolitan_name))
    
    
@ui_api.route('/genres')
def genre_list():
    genre_query = Genres.query.order_by(Genres.name).all()
    genres = []

    # TODO: Create service
    for genre in genre_query:
        genres.append({
            'id': genre.id,
            'name': genre.name,
        })

    return jsonify({
        'data': genres
    })

    
@ui_api.route('/metropolitans')
def metropolitan_list():
    metro_query = MetropolitanArea.query.all()
    metro_areas = []
    
    for area in metro_query:
        metro_areas.append({
            'id': area.id,
            'name': area.name,
        })
    
    return jsonify({
        'data': metro_areas
    })
    
# @app.route('/venues')
# def venue_list():
#     #Venues.query.filter(Venues.venue_id == event.venue_id).one_or_none()
#     return None

app.register_blueprint(ui_api)