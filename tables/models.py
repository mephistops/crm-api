from datetime import date, datetime
from pydantic import BaseModel


class UserIn(BaseModel):
    firstname: str
    lastname: str
    mail: str
    password: str


class User(BaseModel):
    id: int
    firstname: str
    lastname: str
    mail: str
    password: str


class ContactIn(BaseModel):
    firstname: str
    lastname: str
    mail: str
    phone: str
    birthday: date
    address: str
    contact_type: int
    origin: int
    gender: int


class Contact(BaseModel):
    id: int
    firstname: str
    lastname: str
    mail: str
    phone: str
    birthday: date
    address: str
    contact_type: int
    origin: int
    gender: int


class CommentIn(BaseModel):
    id_contact: int = None
    comment: str = None


class Comment(BaseModel):
    id: int
    id_contact: int = None
    comment: str = None


class ContactTypeIn(BaseModel):
    description: str


class ContactType(BaseModel):
    id: int
    description: str


class GenderIn(BaseModel):
    description: str


class Gender(BaseModel):
    id: int
    description: str


class OriginIn(BaseModel):
    description: str


class Origin(BaseModel):
    id: int
    description: str


class StatusIn(BaseModel):
    description: str


class Status(BaseModel):
    id: int
    description: str


class Tasks(BaseModel):
    id: int
    title: str
    id_user: int
    date_end: datetime
    status: int
    id_contact: int


class TasksIn(BaseModel):
    title: str
    id_user: int
    date_end: datetime
    status: int
    id_contact: int
