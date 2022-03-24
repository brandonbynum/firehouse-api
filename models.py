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
    
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def serializer(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    
class ArtistGenre(db.Model):
    __tablename__ = 'artist_genre'
    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('Artist.id'))
    genre_id = Column(Integer, ForeignKey('Genre'))
    
    def __init__(self):
        self.id = id
        self.artist_id = artist_id
        self.genre_id = genre_id 
        
    def serializer(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'genre_id': self.genre_id,
        }

    class Meta:
        managed = False
        db_table = 'artist_genre'


class MetropolitanArea(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    
    def __init__(self):
        self.id = id
        self.name = name 
  
    
    def serializer(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    class Meta:
        managed = False
        db_table = 'metropolitan_area'

class Cities(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    state = Column(String(255), nullable=True)
    country = Column(String(255))
    metropolitan_id = Column(Integer, ForeignKey('MetropolitanArea'), nullable=False)
    
    def __init__(self):
        self.id = id
        self.name = name
        self.state = state
        self.country = country
        self.metropolitan_id = metropolitan_id
    
    def serializer(self):
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'country': self.country,
            'metropolitan_id': self.metropolitan_id,
        }
        

    class Meta:
        managed = False
        db_table = 'cities'

class EventArtist(db.Model):
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.event_id'))
    artist_id = Column(Integer, ForeignKey('Artist.id'))
    headliner = Column(Boolean)
    created_at = Column(DateTime)
    
    def __init__(self):
        self.id = id
        self.event_id = event_id
        self.artist_id = artist_id
        self.headliner = headliner
        self.created_at = created_at
    
    def serializer(self):
        return {
            'event_id': self.event_id,
            'artist_id': self.artist_id,
            'headliner': self.headliner,
        }

    class Meta:
        managed = False
        db_table = 'event_artist'


class Events(db.Model):
    id = Column(Integer, primary_key=True)
    venue_id = Column(Integer, ForeignKey('venue.venue_id'), nullable=True)
    name = Column(String)
    start_at = Column(Time, nullable=True, server_default=func.now())
    end_at = Column(Time, nullable=True, server_default=func.now())
    tickets_link = Column(Text, nullable=True)
    date = Column(DateTime, nullable=True, server_default=func.now())
    type = Column(Text)
    created_on = Column(DateTime)
    
    def __init__(self):
        self.id = id
        self.venue_id = venue_id
        self.name = name
        self.start_at = start_at
        self.end_at = end_at
        self.tickets_link = tickets_link
        self.date = date
        self.type = type
        self.created_on = created_on
    
    def serializer(self):
        return {
            'id': self.id,
            'venue_id': self.venue_id,
            'name': self.name,
            'start_at': self.start_at,
            'end_at':self.end_at,
            'tickets_link': self.tickets_link,
            'date': self.date.is_format(),
            'type': self.type,    
        } 

    class Meta:
        managed = False
        db_table = 'events'

class Genres(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    
    def __init__(self):
        self.id = id
        self.name = name
    
    def serializer(self):
        return {
            'id': serializer.id,
            'name': serializer.name,
        }

    class Meta:
        managed = False
        db_table = 'genres'


class Venues(db.Model):
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('Cities'), nullable=True)
    name = Column(String(255))
    address = Column(String(255))
    
    def __init__(self):
        self.id = id
        self.city_id = city_id
        self.name = name
        self.address = address
    
    def serializer(self):
        return {
            'name': self.name,
            'address': self.address,
        }

    class Meta:
        managed = False
        db_table = 'venues'
