from operator import attrgetter
from operator import itemgetter
from utilities import pretty_print

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
        all_filters = []
        event_list = []

        if metro:
            all_filters.append(MetropolitanArea.name == metro)
                        
        query = Events.query\
            .filter(*all_filters)\
            .join(EventArtist, Events.id == EventArtist.event_id)\
            .join(Artist, EventArtist.artist_id == Artist.id)\
            .join(ArtistGenre, Artist.id == ArtistGenre.artist_id)\
            .join(Genres, ArtistGenre.genre_id == Genres.id)\
            .join(Venues, Events.venue_id == Venues.id)\
            .join(Cities, Venues.city_id == Cities.id)\
            .add_columns(
                Events.id, 
                Events.date, 
                Events.type,
                Events.tickets_link, 
                EventArtist.headliner,
                Artist.name.label('artist_name'),
                Cities.name.label('city_name'),
                Genres.name.label('genre_name'),
                Venues.name.label('venue_name'),
            ).all()

        for row in query:
            print(row)

        # Map data rows to UI models by event id and add to response list
        for row in query: 
            # artist_dict = {
            #     'name': row.artist_name,
            #     'headliner': row.headliner,
            # }  
            # event_id = row.id
            # event_index_dict = {event_list[index]['id']: index for index, event in enumerate(event_list)}
            
            # Code to return all artists under respective event
            # if event_id in event_index_dict.keys():
            #     event_index = event_index_dict[event_id]
            #     event_genres = event_list[event_index]['genres']
            #     event_artists = event_list[event_index]['artists']
            #     genre_name = row.genre_name
                
            #     if artist_dict['name'] not in [artist['name'] for artist in event_artists]:
            #         event_artists.append(artist_dict)
            #         event_list[event_index]['artists'] = sorted(event_artists, key=itemgetter('is_headliner'), reverse=True)

            #     if genre_name not in event_genres:
            #         event_genres.append(genre_name)
            # else:   
            #     event_list.append({
            #         'event_id': row.event_id,
            #         'artists': [artist_dict],
            #         'genres': [row.genre_name],
            #         'date': row.event_date,
            #         'start_at': row.event_start_at,
            #         'tickets_url': row.tickets_link,
            #         'type': row.event_type,
            #         'venue_name': row.venue_name,
            #     })

            event_list.append({
                'event_id': row.id,
                'artist': {
                    'name': row.artist_name,
                    'headliner': row.headliner
                },
                'city': row.city_name,
                'genre': row.genre_name,
                'date': row.date,
                'tickets_url': row.tickets_link,
                'type': row.type,
                'venue': row.venue_name,
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