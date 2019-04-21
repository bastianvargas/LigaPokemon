
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from aplication.app import db




class League(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    position_table = relationship("Position_Table", uselist=False, back_populates="League")

class Trainer(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    pokemons = relationship("pokemon")

class Pokemon(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    hp = Column(Integer)
    speed = Column(Integer)
    attack = Column(Integer)
    trainer_id = Column(Integer, ForeignKey('trainer.id'))

class Position_Table(db.Model):
    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    league_id = Column(Integer, ForeignKey('league.id'))
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    trainer = relationship("League", back_populates="position_table")
