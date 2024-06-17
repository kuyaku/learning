########### INSERT ###############
# For both Core and ORM perspective, the SQL INSERT statement is generated directly using the insert() function. This function generate a new instance of Insert, to add new data into a table

# 1. with the core perspective
# (When using the ORM, we normally use another tool that rides on top, called as unit of work, which will automate the production of many INSERT statements at once.

# The insert() SQL Expresssion Construct
from database_metadata import user_table, address_table, User
from sqlalchemy import insert, select
from basics.config import engine

stmt = insert(user_table).values(name='Happy', fullname='Happy Singh')
print(stmt, type(stmt))

compiled = stmt.compile()
print(compiled, type(compiled))
print(compiled.params)

# executing the statement
with engine.connect() as conn:
    result = conn.execute(stmt)
    # by default the insert statement does not return any rows, and if only a single row is inserted, it will usually include the ability to return information
    # about the column-level default values (like primary key(s)) that were generated during the INSERT of that row.
    print(result.inserted_primary_key)
    conn.commit()

# we don't need to pass values while defining statement, it can be passed while execution. By default the INSERT statement created will contain all the fields of column of the table
print(insert(user_table))

with engine.connect() as conn:
    # the execute many form, dictionary or the list of dictionary
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy veer"},
            {"name": "sandy2", "fullname": "Sandy2 veer"}
        ]
    )
    conn.commit()


# Returning statement
# in general, the returning statement for supported backends is used automatically in order to retrieve the last inserted primary key value as well as the values for server defaults.
# However, the returning clause may also be specified explicitly using the Insert.returning() method. In this case the Result Object has rows which can be fetched.\

insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)

print(insert_stmt)

# the returning clause is also supported by UPDATE and DELETE

# bulk INSERT with or without RETURNING is also supported by the ORM.





############### SELECT #########################

stmt = select(user_table).where(user_table.c.name == 'Happy')
print(stmt)


with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(row)


# with the ORM
# stmt = select(User).where(User.name == 'Happy')
# with Session(engine) as session:
#     result = session.execute(stmt)
#     for row in result:
#         print(row)