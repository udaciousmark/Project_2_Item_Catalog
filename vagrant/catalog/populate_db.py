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
        { "name": "Ski Gloves" },
        { "name": "Ski Goggles" },
        { "name": "Ski Jacket" },
        { "name": "Ski poles" },
        { "name": "Skis" },
    ]
})
category_items.append({
    "category": "Snowboarding",
    "items": [
        { "name": "Snowboarding Gloves" },
        { "name": "Snowboarding Goggles" },
        { "name": "Snowboarding Jacket" },
        { "name": "Snowboard" },
    ]
})
category_items.append({
    "category": "Soccer",
    "items": [
        { "name": "Soccer Ball" },
        { "name": "Soccer Gloves" },
        { "name": "Soccer Goal Post" },
        { "name": "Soccer Shin Guards" },
        { "name": "Soccer Uniform" },
    ]
})
category_items.append({
    "category": "Tennis",
    "items": [
        { "name": "Tennis Balls (3-pack)" },
        { "name": "Tennis Hat" },
        { "name": "Tennis Headband" },
        { "name": "Tennis Racket" },
        { "name": "Tennis Shirt (black)" },
        { "name": "Tennis Shirt (white)" },
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
