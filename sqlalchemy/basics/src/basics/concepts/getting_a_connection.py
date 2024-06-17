from sqlalchemy import text
# without the sqlalchemy expression language, we are making use of the text() construct
# Text allows us to write SQL statements as Textual SQL
from basics.config import engine
## The purpose of engine


# The sole purpose of the engine object from a user-facing perspective is to provide a unit of connectivity to the database called as "Connection"
# When working with Core directly, the Connection object is how all interaction with the database is done.
# As connection represents an open resource against the database, we want to always limit the scope of our use of this object, and the best way to do that is using "python context manager", using the 'with' statement. It is the portal to the database, should be used cautiously. If you define engine.connect() at the very top or globally, it can be used by anything, which is not a good thing. It should be used by the certain section of the code where it is necessary.

# engine.connect() spit out a Connection object
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

# the result is a Result object

# by default, the transaction is always in progress, and the rollback is processed when the connection is released at the end of scope
# The transaction is not committed automatically, we have to do that explicitly

# example with commit as you go

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"), [{"x": 1, "y": 1}, {"x": 2, "y": 1}],)
    conn.commit()


# example with commit as implicit at the end (if everything goes well), else ROLLBACK

# we use engine.begin() here as a distinction

with engine.begin() as conn:
    conn.execute(text("INSERT INTO some_table (x, y) values (:x, :y)"), [{"x": 8, "y": 2}, {"x": 9, "y": 10},])




# querying into database, and understanding the result object returned by conn.execute

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f'x: {row.x} y: {row.y}')


# sending parameters,
# the conn.execute accepts as second argument the parameters, example
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x}, y: {row.y}")


### IMPORTANT
# Although we don't use textual SQL commands directly in sqlAlchemy, but for the matter of fact, we should never pass python literals (integers, string, etc) directly into sql strings, rather use parameter as above


# as like working with ORM session

from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")

with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}, y: {row.y}")
