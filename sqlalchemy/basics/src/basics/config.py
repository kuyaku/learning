from sqlalchemy import create_engine

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# 3 section to connection string (first arg): the database (name of the database) + the database driver + how to locate the database (here: memory)
# echo=True, to spit out the SQL statements processed while running

# the create_engine doesn't actually try to connect to the database as it is defined, it happens only the first time it is asked to perform an operation
# this programming style is called as lazy initialization



################# 
# with the engine object is ready, we can make basic operation
# the primary interactive endpoints of an engine are:
# 1. Connection
# 2. Result

# There is actually an ORM's facade for these objects, called as Session

# When using an orm, the engine is managed by another object called as session.