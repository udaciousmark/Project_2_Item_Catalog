from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

DB_NAME = 'catalog'

engine = create_engine('postgresql+psycopg2:///' + DB_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

category_items = []

category_items.append({
    "category": "Skiing",
    "items": [
        { "name": "Gloves" },
        { "name": "Goggles" },
        { "name": "Jacket" },
        { "name": "Ski poles" },
        { "name": "Skis" },
    ]
})
category_items.append({
    "category": "Snowboarding",
    "items": [
        { "name": "Gloves" },
        { "name": "Goggles" },
        { "name": "Jacket" },
        { "name": "Snowboard" },
    ]
})
category_items.append({
    "category": "Soccer",
    "items": [
        { "name": "Ball" },
        { "name": "Gloves" },
        { "name": "Goal Post" },
        { "name": "Shin Guards" },
        { "name": "Uniform" },
    ]
})
category_items.append({
    "category": "Tennis",
    "items": [
        { "name": "Balls (3-pack)" },
        { "name": "Hat" },
        { "name": "Headband" },
        { "name": "Racket" },
        { "name": "Shirt (black)" },
        { "name": "Shirt (white)" },
    ]
})

for x in category_items:
    category = Category(name = x['category'])
    session.add(category)
    session.commit()

    for y in x['items']:
        item = Item(name = y['name'], category = category)
        session.add(item)
        session.commit()
