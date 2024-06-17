# when you know about engine and sql execution, we are ready to begin some alchemy.

# the central element of both SQLAlchemy Core and ORM is the SQL expression language

# At the base are the python objects that represents database concepts like tables and columns. These objects collectively are called as database metadata.

# The most common foundational objects for database metadata in SQLAlchemy are
# 1. MetaData
# 2. Table
# 3. Column

# The table is the basic data holding structure in a database.
# In SQLAlchemy, the table is ultimately represented by a Python object also named as "Table"

# Ways to make these "Tables", they are made programatically:
# 1. Directly using the Table Constructor
# 2. Indirectly using the ORM mapped classes

# 3. There is also an option to load some or all table information from an existing database, called as reflection.

# Whichever kind of approach is used, we always start out with a collection that will be where we place our tables, known as MetaData object.
# The Metadata object is just a facade around the Python dictionary.

# The ORM gives some options to get this object, but we can make it directly also as below.

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from basics.config import engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import insert

from typing import List, Optional

metadata_obj = MetaData()

# once we have metadata object, we can define some Table objects.

# making table directly using the Table constructor
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

# String, Integer are classes that represent SQL data types, and can be instantiated or not

# When do I make MetaData object in my program?
# It is ok to have same MetaData object for entire application. This is somewhat related to grouping of tables.

# accessing column objects

# print(user_table.c.keys())
# print(user_table.c["name"])

# print(user_table.primary_key)


# another table of addresses

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)

# we have constructed an object structure that represent two tables in a database,
# starting at the root MetaData object, then into two Table objects, and then Columns, Constraints.
# This object structure will be at the center of most operations we perform with both Core and ORM going forward.


# now the first useful thing which we can do with this structure, is to emit CREATE TABLE statements, which can be done using the metadata object

metadata_obj.create_all(engine)

# the create process also takes care of the fact that some tables are to be created before than others like depending on the foreign keys
# in more complex scenarios, the foreign keys can be applied after creation, using ALTER, that is automatic


# the CREATE / DROP feature of MetaData is useful for test suites, small or new applications. But for real application which gets modification along the way,
# the schema management tools such as Alembic, which build upon SQLAlchemy, are better choices. It is used to make migrations.




######### 
# another way of making Tables, using ORM Declarative forms to define table metadata

# when using ORM, the MetaData collection remains present, however it is associated with an ORM-only construct commonly referred towards as the Declarative Base, so make a Base class, inheriting from DeclarativeBase from orm, and then use it for all models

class Base(DeclarativeBase):
    pass

# now each class using Base class will be ORM mapped class, with each referring to Table object

# The declarative base provides us the MetaData collection by default, we don't have to pass it from outside,
# and can be accessed using Base.metadata

print(Base.metadata)


# declaring Mapped classes

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
    
class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    

Base.metadata.create_all(engine)


################# Working with data ##################

# this is how things work at the core level

# insert

stmt = insert(user_table).values(name='Kunwar', fullname="Kunwar Yatesh")
# now we are using these, and not the text(sql query)

print(stmt) # it is the SQL query we were writing with the text()

compiled = stmt.compile()

print(compiled.params)

with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()


# we don't explicitly use the .values with the insert construct
# the values can be passed while executing the query, the insert(table_name) will generate the query for all columns to insert into

print(insert(user_table))

with engine.connect() as conn:
    result = conn.execute(insert(user_table), [
        {"name": "Abc", "fullname": "Kumar"},
        {"name": "XYZ", "fullname": "Goyal"}
    ],)
    conn.commit()
