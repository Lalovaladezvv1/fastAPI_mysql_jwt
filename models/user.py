from sqlalchemy import Table, engine
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import meta, engine

users = Table("users", meta, Column(
    "id", Integer, primary_key=True), 
    Column("name", String(255)),
    Column("email", String(255)), 
    Column("password", String(255)))


meta.create_all(engine)