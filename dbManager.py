import asyncpg

async def connection(db, credentials):
    return await asyncpg.create_pool(**credentials)

async def setup(db):
    await db.execute("CREATE TABLE IF NOT EXISTS events(name text PRIMARY KEY, description text);")
    await db.execute("CREATE TABLE IF NOT EXISTS events_members(name_event text REFERENCES events, name_member text, PRIMARY KEY(name_event, name_member));")
