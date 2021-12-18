import dataclasses as dc
import typing as tp

import db
# import typing as tp
# from sqlalchemy.orm import class_mapper, ColumnProperty
# from sqlalchemy import UniqueConstraint


@dc.dataclass
class Author:
    __tablename__ = 'author'
    id: int
    name: str
    birth_date: str


@dc.dataclass
class Country:
    __tablename__ = 'country'
    id: int
    name: str


@dc.dataclass
class Death:
    __tablename__ = 'death'
    id: int
    death: str


@dc.dataclass
class Work:
    __tablename__ = 'work'
    id: int
    release_date: str
    title: str
    type: str


@dc.dataclass
class CountryToAuthor:
    __tablename__ = 'country_to_work'
    country_id: int
    author_id: int


@dc.dataclass
class CountryToWork:
    __tablename__ = 'country_to_work'
    country_id: int
    work_id: int


@dc.dataclass
class AuthorToWork:
    __tablename__ = 'author_to_work'
    author_id: int
    work_id: int

#
# # Creating an assisting table Role for Many To Many relation
#
#
# class Role(db.Model):
#     __tablename__ = "Role"
#     uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     author_id = db.Column(db.ForeignKey('Person.uid'))
#     film_id = db.Column(db.ForeignKey('Film.uid'))
#     role = db.Column(db.String(50))
#     person = db.relationship("Person", back_populates="films")
#     film = db.relationship("Film", back_populates="people")
#     UniqueConstraint(role, author_id, film_id, name="uniq_pers_film")
#
#
# class Person_Country(db.Model):
#     __tablename__ = "Person_Country"
#     uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     author_id = db.Column(db.ForeignKey('Person.uid'))
#     country_id = db.Column(db.ForeignKey('Country.uid'))
#     person = db.relationship("Person", back_populates="countries")
#     country = db.relationship("Country", back_populates="people")
#
#
# class Film_Country(db.Model):
#     __tablename__ = "Film_Country"
#     uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     film_id = db.Column(db.ForeignKey('Film.uid'))
#     country_id = db.Column(db.ForeignKey('Country.uid'))
#     film = db.relationship("Film", back_populates="countries")
#     country = db.relationship("Country", back_populates="films")
#
#
# class Country(db.Model):
#     __tablename__ = "Country"
#     uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50), unique=True)
#     people = db.relationship("Person_Country", back_populates="country")
#     films = db.relationship("Film_Country", back_populates="country")
#
#
# def create_country(name):
#     country = Country(name=name)
#     db.session.add(country)
#     db.session.commit()
#
#     return country
#
#
# class Person(db.Model):
#     __tablename__ = "Person"
#     uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     firstname_lastname = db.Column(db.String(150))
#     birth = db.Column(db.Integer)
#     films = db.relationship("Role", back_populates="person")
#     countries = db.relationship("Person_Country", back_populates="person")
#
#     def __init__(self, firstname_lastname, birth=None):
#         self.firstname_lastname = firstname_lastname
#         self.birth = birth
#
#     def __str__(self):
#         return f"{self.firstname_lastname}"
#
#     def columns(self):
#         """Return the actual columns of a SQLAlchemy-mapped object"""
#         return [prop.key for prop in class_mapper(self.__class__).iterate_properties
#                 if isinstance(prop, ColumnProperty)]
#
#
# def create_person(**kwargs):
#     person = Person(**kwargs)
#     db.session.add(person)
#     db.session.commit()
#
#     return person
#
#
# def create_film(**kwargs):
#     film = Film(**kwargs)
#     db.session.add(film)
#     db.session.commit()
#     return film
#
#
# class Film(db.Model):
#     __tablename__ = "Film"
#     uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(50))
#     birth = db.Column(db.Integer)
#     description = db.Column(db.String(150))
#     people = db.relationship("Role", back_populates="film")
#     countries = db.relationship("Film_Country", back_populates="film")
#
#     def __str__(self):
#         return f"{self.name}"
#
#     def columns(self):
#         """Return the actual columns of a SQLAlchemy-mapped object"""
#         return [prop.key for prop in class_mapper(self.__class__).iterate_properties
#                 if isinstance(prop, ColumnProperty)]
#
#
# if __name__ == "__main__":
#     # Run this file directly to create the database tables.
#     print("Creating database tables...")
#     db.create_all()
#     print("Done!")
#
# # from models import Person, Role, Film
# # p = Person(firstname="Test2", username="Test2")
# # f = Film(name="Test2")
# # r = Role(role="Director")
# # r.film = f
# # p.films.append(r)
# # from app import db
