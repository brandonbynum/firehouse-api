from flask import jsonify
from sqlalchemy import func

import models

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
        
    def get_event_details(self, genre, metro):
        artist_genre_query = None
        event_artist_query = None
        cities_query = None
        events_query = None
        genre_query = None
        metro_query = None
        venues_query = None
        
        event_details = []

        if metro:
            metro_query = self.Metropolitan_Area.query.filter(
                func.lower(self.Metropolitan_Area.metropolitan_name) == metro.lower()
            ).one_or_none()
            
            cities_query = self.Cities.query.filter_by(
                metropolitan_id=metro_query.metropolitan_id
            ).all()
            city_ids = [city.city_id for city in cities_query]

            venues_query = self.Venues.query.filter(
                self.Venues.city_id.in_(city_ids))
            venue_ids = [venue.venue_id for venue in venues_query]
            events_query = self.Events.query.filter(
                self.Events.venue_id.in_(venue_ids))
            
        if genre:
            # TODO: 404 or none on events query
            genre_query = self.Genres.query.filter(
                func.lower(self.Genres.genre_name) == genre.lower()).one_or_none()
            
            artist_genre_query = self.ArtistGenre.query.filter(
                self.ArtistGenre.genre_id == genre_query.genre_id)
            artist_ids = [artist_genre.artist_id for artist_genre in artist_genre_query]
            artists_query = self.Artist.query.filter(
                self.Artist.artist_id.in_(artist_ids))
            artists = {artist.artist_id: artist.serializer() for artist in artists_query}
            
            event_artist_query = self.Event_Artist.query.filter(
                self.Event_Artist.artist_id.in_(artist_ids))   
            event_ids = [event_artist.event_id for event_artist in event_artist_query]
            events_query = self.Events.query.filter(
                self.Events.event_id.in_(event_ids))
                
        if not metro and not genre:
            events_query = self.Events.query.all()
            
        events = [event for event in events_query]
        for event in events_query:
            event_id = event.event_id
            print(event_id)
            
            # TODO?: List respective genres under each artist
            event_artist_query = self.Event_Artist.query.filter(
                self.Event_Artist.event_id == event_id).all()
            if event_artist_query:
                artist_id_and_bids = {item.artist_id: item.is_headliner for item in event_artist_query}
                artist_ids = list(artist_id_and_bids.keys())
                artists_query = self.Artist.query.filter(
                    self.Artist.artist_id.in_(artist_ids))
                artist_data = [{**artist.serializer(), 'headliner': artist_id_and_bids[artist.artist_id]} 
                            for artist in artists_query]
            else:
                continue
                    
                
            artist_genre_query = self.ArtistGenre.query.filter(
                self.ArtistGenre.artist_id.in_(artist_ids)).all()
            genre_ids = [item.genre_id for item in artist_genre_query]
            genre_query = self.Genres.query.filter(
                self.Genres.genre_id.in_(genre_ids)).all()

            venues_query = self.Venues.query.filter(
                self.Venues.venue_id == event.venue_id).one_or_none()
            cities_query = self.Cities.query.filter(
                self.Cities.city_id == venues_query.city_id).one_or_none()
            metro_query = self.Metropolitan_Area.query.filter(
                self.Metropolitan_Area.metropolitan_id == cities_query.metropolitan_id).one_or_none()
                
            event_details.append({
                'id': event_id,
                'artists': artist_data,
                'date': event.event_date,
                'end_at': str(event.event_end_at),
                'genres': [item.genre_name for item in genre_query],
                'name': event.event_name,
                'metro': metro_query.metropolitan_name,
                'start_at': str(event.event_start_at),
                'tickets_url': event.tickets_link,
                'type': event.event_type,
                'venue': venues_query.serializer(),
            })
            
        return jsonify({'data': event_details})