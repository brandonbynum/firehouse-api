from flask import jsonify
from sqlalchemy import func
import json
import datetime
import models
from utilities.pretty_print import pretty_print

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
        
    def upcoming_events_test(self, genre=None, metro=None):
        all_filters = []
        if metro:
            all_filters.append(self.Metropolitan_Area.metropolitan_name == metro)
        if genre:
            all_filters.append(self.Genres.genre_name == genre)
            
        print(all_filters)
            
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
            
        res = []
        for row in query:
            res.append({
                'artist': {
                    'name': row.artist_name,
                    'is_headliner': row.is_headliner,
                },
                'event_id': row.event_id,
                'genres': row.genre_name,
                'date': row.event_date,
                'start_at': row.event_start_at,
                'tickets_url': row.tickets_link,
                'type': row.event_type,
                'venue': {
                    'name': row.venue_name,
                    'address': row.venue_address
                },
                
            })
        return res