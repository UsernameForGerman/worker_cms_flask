import dataclasses as dc
import typing as tp

import db


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
