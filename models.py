from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Time
from sqlalchemy.sql import func
from flask_migrate import Migrate
import json

db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

class Artist(db.Model):
    __tablename__ = 'artists'
    
    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String)

    def __init__(self, artist_id, artist_name):
        self.artist_id = artist_id
        self.artist_name = artist_name
      
    def __repr_(self):
        return f'<Artist {self.artist_name!r}>'  
    
    def serializer(self):
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist_name,
        }
    
class ArtistGenre(db.Model):
    artist_genre_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('Artist'))
    genre_id = Column(Integer, ForeignKey('Genre'))
    
    def __init__(self):
        self.artist_genre_id = artist_genre_id
        self.artist_id = artist_id
        self.genre_id = genre_id
        
    def __repr_(self):
        return {
            'id': self.artist_genre_id,
            'artist_id': self.artist_id,
            'genre_id': self.genre_id,
        }  
        
    def serializer(self):
        return {
            'id': self.artist_genre_id,
            'artist_id': self.artist_id,
            'genre_id': self.genre_id,
        }

    class Meta:
        managed = False
        db_table = 'artist_genre'


class MetropolitanArea(db.Model):
    metropolitan_id = Column(Integer, primary_key=True)
    metropolitan_name = Column(String(50))
    
    def __init__(self):
        self.metropolitan_id = metropolitan_id
        self.metropolitan_name = metropolitan_name
        
    def __repr_(self):
        return f'<MetropolitanArea {self.metropolitan_name!r}>'  
    
    
    def serializer(self):
        return {
            'metropolitan_id': self.metropolitan_id,
            'metropolitan_name': self.metropolitan_name,
        }
    class Meta:
        managed = False
        db_table = 'metropolitan_area'

class Cities(db.Model):
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String(255))
    city_state = Column(String(255), nullable=True)
    city_country = Column(String(255))
    metropolitan_id = Column(Integer, ForeignKey('MetropolitanArea'), nullable=False)
    
    def __init__(self):
        self.city_id = city_id
        self.city_name = city_name
        self.city_state = city_state
        self.city_country = city_country
        self.metropolitan_id = metropolitan_id
    
    def __repr_(self):
        return f'<Cities {self.city_name!r}>'  
    
    def serializer(self):
        return {
            'city_id': self.city_id,
            'city_name': self.city_name,
            'city_state': self.city_state,
            'city_country': self.city_country,
            'metropolitan_id': self.metropolitan_id,
        }
        

    class Meta:
        managed = False
        db_table = 'cities'

class EventArtist(db.Model):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    is_headliner = Column(Boolean)
    created_at = Column(DateTime)
    
    def __init__(self):
        self.id = id
        self.event_id = event_id
        self.artist_id = artist_id
        self.is_headliner = is_headliner
        self.created_at = created_at
        
    def __repr_(self):
        return {
            'event_id': self.event_id,
            'artist_id': self.artist_id,
            'headliner': self.is_headliner,
        } 
    
    def serializer(self):
        return {
            'event_id': self.event_id,
            'artist_id': self.artist_id,
            'headliner': self.is_headliner,
        }

    class Meta:
        managed = False
        db_table = 'event_artist'


class Events(db.Model):
    event_id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venue.venue_id'), nullable=True)
    event_name = Column(String)
    event_start_at = Column(Time, nullable=True, server_default=func.now())
    event_end_at = Column(Time, nullable=True, server_default=func.now())
    tickets_link = Column(Text, nullable=True)
    event_date = Column(DateTime, nullable=True, server_default=func.now())
    event_type = Column(Text)
    created_on = Column(DateTime)
    
    def __init__(self):
        self.event_id = event_id
        self.venue_id = venue_id
        self.event_name = event_name
        self.event_start_at = event_start_at
        self.event_end_at = event_end_at
        self.tickets_link = tickets_link
        self.event_date = event_date
        self.event_type = event_type
        self.created_on = created_on

    def __repr_(self):
        return {
            'event_id': self.event_id,
            'venue_id': self.venue_id,
            'event_name': self.event_name,
            'event_start_at': self.event_start_at,
            'event_end_at':self.event_end_at,
            'tickets_link': self.tickets_link,
            'event_date': self.event_date.is_format(),
            'event_type': self.event_type,    
        } 
    
    def serializer(self):
        return {
            'event_id': self.event_id,
            'venue_id': self.venue_id,
            'event_name': self.event_name,
            'event_start_at': self.event_start_at,
            'event_end_at':self.event_end_at,
            'tickets_link': self.tickets_link,
            'event_date': self.event_date.is_format(),
            'event_type': self.event_type,    
        } 

    class Meta:
        managed = False
        db_table = 'events'


class Genres(db.Model):
    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(50), nullable=True)
    
    def __init__(self):
        self.genre_id = genre_id
        self.genre_name = genre_name
    
    def __repr_(self):
        return f'<Genres {self.genre_name!r}>'  
    
    def serializer(self):
        return {
            'id': serializer.genre_id,
            'name': serializer.genre_name,
        }

    class Meta:
        managed = False
        db_table = 'genres'


class Venues(db.Model):
    venue_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('Cities'), nullable=True)
    venue_name = Column(String(255))
    venue_address = Column(String(255))
    
    def __init__(self):
        self.venue_id = venue_id
        self.city_id = city_id
        self.venue_name = venue_name
        self.venue_address = venue_address

    def __repr_(self):
        return f'<Venues {self.venue_name!r}>'
    
    def serializer(self):
        return {
            'name': self.venue_name,
            'address': self.venue_address,
        }

    class Meta:
        managed = False
        db_table = 'venues'
