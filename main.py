from typing import List
import databases
from sqlalchemy import select, MetaData, create_engine, Table, Column, Integer, String, DateTime

from tables.models import ContactIn, GenderIn, User, Contact, Tasks, TasksIn, Comment, CommentIn, ContactType, Gender, Origin, Status

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

database = databases.Database("sqlite:///./crm.db")
metadata = MetaData()

engine = create_engine("sqlite:///./crm.db", connect_args={"check_same_thread": False})

metadata.create_all(engine)

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('firstname', String),
              Column('lastname', String),
              Column('mail', String, unique=True),
              Column('password', String),
              )

contacts = Table('contacts', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('firstname', String),
                 Column('lastname', String),
                 Column('mail', String, unique=True),
                 Column('phone', String),
                 Column('birthday', DateTime),
                 Column('address', String),
                 Column('contact_type', Integer),
                 Column('origin', Integer),
                 Column('gender', Integer)
                 )

tasks = Table('tasks', metadata,
              Column('id', Integer, primary_key=True),
              Column('title', String),
              Column('id_user', Integer),
              Column('date_end', DateTime),
              Column('status', Integer),
              Column('id_contact', Integer),
              Column('created_at', DateTime),
              )

comments = Table('comments', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('id_contact', Integer),
                 Column('comment', String)
                 )

contact_types = Table('contact_types', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('description', String)
                      )

gender = Table('gender', metadata,
               Column('id', Integer, primary_key=True),
               Column('description', String)
               )

origin = Table('origins', metadata,
               Column('id', Integer, primary_key=True),
               Column('description', String)
               )

status = Table('status', metadata,
               Column('id', Integer, primary_key=True),
               Column('description', String)
               )

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/contacts/", response_model=List[Contact])
async def read_contacts():
    query = contacts.select()
    return await database.fetch_all(query)


@app.get("/contact/", response_model=Contact)
async def read_one_contact(contact_id: int):
    if(contact_id == 0 or contact_id == None):
        return {"message": "Contact not found"}
    query = contacts.select().where(contacts.c.id == contact_id)
    return await database.fetch_one(query)


@app.put("/contacts/", response_model=Contact)
async def update_contact(contact: Contact):
    query = contacts.update().values(
        firstname=contact.firstname,
        lastname=contact.lastname,
        mail=contact.mail,
        phone=contact.phone,
        birthday=contact.birthday,
        address=contact.address,
        contact_type=contact.contact_type,
        origin=contact.origin,
        gender=contact.gender
    ).where(contacts.c.id == contact.id)
    last_record_id = await database.execute(query)
    return {**contact.dict(), 'id': last_record_id}


@app.post("/contacts/", response_model=Contact)
async def create_contact(contact: ContactIn):
    query = contacts.insert().values(
        firstname=contact.firstname,
        lastname=contact.lastname,
        mail=contact.mail,
        phone=contact.phone,
        birthday=contact.birthday,
        address=contact.address,
        contact_type=contact.contact_type,
        origin=contact.origin,
        gender=contact.gender
    )
    last_record_id = await database.execute(query)
    return {**contact.dict(), 'id': last_record_id}


@app.delete("/contacts/{contact_id}")
async def delete_contact(contact_id):
    query = contacts.delete().where(contacts.c.id == contact_id)
    await database.execute(query)
    return {'message': 'Contact deleted'}


@app.get("/contact_types/", response_model=List[ContactType])
async def read_contact_types():
    query = contact_types.select()
    return await database.fetch_all(query)

@app.get("/comments/", response_model=List[Comment])
async def read_comments(contact_id: int):
    query = comments.select().where(comments.c.id_contact == contact_id)
    return await database.fetch_all(query)

@app.get("/comment/", response_model=Comment)
async def read_comment(id_comment: int):
    query = comments.select().where(comments.c.id == id_comment)
    return await database.fetch_one(query)

@app.post("/comments/", response_model=Comment)
async def create_comment(commentIn: CommentIn):
    query = comments.insert().values(
        id_contact=commentIn.id_contact,
        comment=commentIn.comment
    )
    last_record_id = await database.execute(query)
    return {**commentIn.dict(), 'id': last_record_id}

@app.put("/comments/", response_model=Comment)
async def edit_comment(commentIn: Comment):
    query = comments.update().values(
        comment=commentIn.comment
    ).where(comments.c.id == commentIn.id)
    last_record_id = await database.execute(query)
    return {**commentIn.dict(), 'id': last_record_id}

@app.delete("/comments/{id_comment}")
async def delete_contact(id_comment):
    query = comments.delete().where(comments.c.id == id_comment)
    await database.execute(query)
    return {'message': 'Comment deleted'}

@app.get("/gender/", response_model=Gender)
async def read_gender_by_id(id: int):
    query = gender.select().where(gender.c.id == id)
    return await database.fetch_one(query)


@app.get("/genders/", response_model=List[Gender])
async def read_genders():
    query = gender.select()
    return await database.fetch_all(query)


@app.post("/gender/", response_model=Gender)
async def create_gender(genderIn: GenderIn):
    query = gender.insert().values(
        description=genderIn.description
    )
    last_record_id = await database.execute(query)
    return {**genderIn.dict(), 'id': last_record_id}


@app.get("/origins/", response_model=List[Origin])
async def read_origins():
    query = origin.select()
    return await database.fetch_all(query)


@app.get("/status/", response_model=List[Status])
async def read_status():
    query = status.select()
    return await database.fetch_all(query)


@app.get("/tasks/")
async def read_tasks(id_contact: int):
    query = select(tasks.c.id, tasks.c.title, users.c.firstname, users.c.lastname, tasks.c.date_end,
                   tasks.c.created_at).where(tasks.c.id_contact == id_contact, users.c.id == tasks.c.id_user)
    return await database.fetch_all(query)

@app.get("/task/")
async def read_task(id_task: int):
    query = select(tasks.c.id, tasks.c.title, users.c.id, users.c.firstname, users.c.lastname, tasks.c.date_end,
                   tasks.c.created_at).where(tasks.c.id == id_task)
    return await database.fetch_one(query)

@app.put("/tasks/", response_model=Tasks)
async def update_task(task: Tasks):
    query = tasks.update().values(
        title=task.title,
        id_user=task.id_user,
        date_end=task.date_end,
    ).where(tasks.c.id == task.id)
    last_record_id = await database.execute(query)
    return {**task.dict(), 'id': last_record_id}


@app.post("/tasks/", response_model=Tasks)
async def create_task(task: TasksIn):
    query = tasks.insert().values(
        title=task.title,
        id_user=task.id_user,
        date_end=task.date_end,
        status=task.status,
        id_contact=task.id_contact
    )
    last_record_id = await database.execute(query)
    return {**task.dict(), 'id': last_record_id}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': 'Task deleted'}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/user/", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_all(query)
