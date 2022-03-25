from operator import attrgetter
from operator import itemgetter
from utilities import pretty_print
from datetime import datetime
from sqlalchemy import func

from models import Artist
from models import ArtistGenre
from models import Cities
from models import Events
from models import EventArtist
from models import Genres
from models import MetropolitanArea
from models import Venues

class EventService():
    # def __init__(self):
    #     self.Artist = models.Artist
    #     self.ArtistGenre = models.ArtistGenre
    #     self.Cities = models.Cities
    #     self.Events = models.Events
    #     self.EventArtist = models.EventArtist
    #     self.Genres = models.Genres
    #     self.MetropolitanArea = models.MetropolitanArea
    #     self.Venues = models.Venues
        
    # TODO: Filter date after now
    def upcoming_events_test(self, metro=None):
        all_filters = [Events.date >= datetime.today()]
        event_list = []

        if metro:
            all_filters.append(func.lower(MetropolitanArea.name) == metro.lower())

        print(f'----------METRO: {metro} ---------------')
                        
        query = Events.query\
            .filter(*all_filters)\
            .join(EventArtist, Events.id == EventArtist.event_id)\
            .join(Artist, EventArtist.artist_id == Artist.id)\
            .join(ArtistGenre, Artist.id == ArtistGenre.artist_id)\
            .join(Genres, ArtistGenre.genre_id == Genres.id)\
            .join(Venues, Events.venue_id == Venues.id)\
            .join(Cities, Venues.city_id == Cities.id)\
            .join(MetropolitanArea, Cities.metropolitan_id == MetropolitanArea.id)\
            .order_by(Events.date)\
            .add_columns(
                Events.id, 
                Events.name.label('event_name'),
                Events.date, 
                Events.type,
                Events.tickets_link, 
                EventArtist.headliner,
                Artist.name.label('artist_name'),
                Cities.name.label('city_name'),
                Genres.name.label('genre_name'),
                Venues.name.label('venue_name'),
            ).all()

        for raw_event in query:
            # Check if event_id/artist.name exists in the list
            # If so, add genre to existing item
            # If not, add item to list
            print('raw_event:', raw_event.id, raw_event.artist_name)
            for hashIndex, hash_event in enumerate(event_list):
                print('hash_event', hash_event['event_id'], hash_event['artist']['name'], '\n')
                if raw_event.id == hash_event['event_id'] and raw_event.artist_name == hash_event['artist']['name']:
                    event_list[hashIndex]['genres'].append(raw_event.genre_name)
                    break
            else:
                event_list.append({
                    'event_id': raw_event.id,
                    'event_name': raw_event.event_name,
                    'artist': {
                        'name': raw_event.artist_name,
                        'headliner': raw_event.headliner
                    },
                    'city': raw_event.city_name,
                    'genres': [raw_event.genre_name],
                    'date': raw_event.date.strftime("%m/%d/%Y"),
                    'tickets_url': raw_event.tickets_link,
                    'type': raw_event.type,
                    'venue': raw_event.venue_name,
                })
        return event_list
    
    def get_event_details(id_to_query):
        artists = []
        event_details = []
        query_res = Events.query.filter(Events.id == id_to_query)\
            .join(EventArtist, Events.id == EventArtist.event_id)\
            .join(Artist, EventArtist.artist_id == Artist.id)\
            .join(Venues, Events.venue_id == Venues.id)\
            .join(Cities, Venues.city_id == Cities.id)\
            .join(MetropolitanArea, Cities.metropolitan_id == MetropolitanArea.id)\
            .add_columns(Events.id, Events.date, Events.type, Events.start_at,
                        Events.end_at, Events.name, Events.tickets_link,
                        Artist.name.label('artist_name'), EventArtist.headliner, Cities.name.label('city_name'), Cities.state, 
                        MetropolitanArea.name.label('metropolitan_name'), Venues.name.label('venue_name'), Venues.address)
        
        for row in query_res:
            event_details.append(row)
            artists.append({
                'name': row.artist_name,
                'headliner': row.headliner,
            })
            artists.sort(key=lambda artist: artist['headliner'], reverse=True)
        
        res = {
            'event_id': query_res[0].id,
            'artists': artists,
            'date': query_res[0].date,
            'end_at': query_res[0].end_at and str(query_res[0].end_at),
            'name': query_res[0].name,
            'metropolitan_area': query_res[0].metropolitan_name,
            'start_at': query_res[0].start_at and str(query_res[0].start_at),
            'tickets_url': query_res[0].tickets_link,
            'type': query_res[0].type,
            'venue': {
                'name': query_res[0].venue_name,
                'address': query_res[0].address,
                'city': query_res[0].city_name,
                'state': query_res[0].state,
            }
        }

        return res