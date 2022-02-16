import models
from operator import attrgetter
from operator import itemgetter


class EventService():
    def __init__(self):
        self.Artist = models.Artist
        self.ArtistGenre = models.ArtistGenre
        self.Cities = models.Cities
        self.Events = models.Events
        self.Event_Artist = models.EventArtist
        self.Genres = models.Genres
        self.Metropolitan_Area = models.MetropolitanArea
        self.Venues = models.Venues
        
    # TODO: Filter date after now
    def upcoming_events_test(self, genre=None, metro=None):
        all_filters = []
        event_list = []

        if metro:
            all_filters.append(self.Metropolitan_Area.metropolitan_name == metro)
        if genre:
            all_filters.append(self.Genres.genre_name == genre)
                        
        query = self.Events.query\
            .filter(*all_filters)\
            .join(self.Event_Artist, self.Events.event_id == self.Event_Artist.event_id)\
            .join(self.Venues, self.Events.venue_id == self.Venues.venue_id)\
            .join(self.Cities, self.Venues.city_id == self.Cities.city_id)\
            .join(self.Metropolitan_Area, self.Cities.metropolitan_id == self.Metropolitan_Area.metropolitan_id)\
            .join(self.Artist, self.Event_Artist.artist_id == self.Artist.artist_id)\
            .join(self.ArtistGenre, self.Artist.artist_id == self.ArtistGenre.artist_id)\
            .join(self.Genres, self.Genres.genre_id == self.ArtistGenre.genre_id)\
            .add_columns(self.Events.event_id, self.Events.event_date, self.Events.event_start_at, self.Events.event_type,
                        self.Events.tickets_link, self.Artist.artist_id, self.Artist.artist_name, self.Event_Artist.is_headliner, 
                        self.Genres.genre_name, self.Venues.venue_id, self.Venues.venue_name, self.Venues.venue_address, 
                        self.Metropolitan_Area.metropolitan_name)\
            .all()
        
        # Map data rows to UI models by event id and add to response list
        for row in query: 
            artist_dict = {
                'name': row.artist_name,
                'is_headliner': row.is_headliner,
            }  
            event_id = row.event_id
            event_index_dict = {event_list[index]['event_id']: index for index, event in enumerate(event_list)}
            
            if event_id in event_index_dict.keys():
                event_index = event_index_dict[event_id]
                event_genres = event_list[event_index]['genres']
                event_artists = event_list[event_index]['artists']
                genre_name = row.genre_name
                
                if artist_dict['name'] not in [artist['name'] for artist in event_artists]:
                    event_artists.append(artist_dict)
                    event_list[event_index]['artists'] = sorted(event_artists, key=itemgetter('is_headliner'), reverse=True)

                if genre_name not in event_genres:
                    event_genres.append(genre_name)
            else:   
                event_list.append({
                    'event_id': row.event_id,
                    'artists': [artist_dict],
                    'genres': [row.genre_name],
                    'date': row.event_date,
                    'start_at': row.event_start_at,
                    'tickets_url': row.tickets_link,
                    'type': row.event_type,
                    'venue': {
                        'name': row.venue_name,
                        'address': row.venue_address
                    },
                })
        return event_list