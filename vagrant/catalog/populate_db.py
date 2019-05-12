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
        { "name": "Ski Gloves", "description": "Gloves to keep your hands warm while moving fast against the cold air" },
        { "name": "Ski Goggles", "description": "Goggles to protect your eyes from the cold air when moving at high speed" },
        { "name": "Ski Jacket", "description": "This jacket is like no other in protecting you from the elements, very warm, yet light enough to not distract you from the joy of skiing" },
        { "name": "Ski poles", "description": "For those that would like a little more control over their balance, these are poles you can rely on" },
        { "name": "Skis", "description": "The best skis you'll ever use!" },
    ]
})
category_items.append({
    "category": "Snowboarding",
    "items": [
        { "name": "Snowboarding Gloves", "description": "A description for this item" },
        { "name": "Snowboarding Goggles", "description": "A description for this item" },
        { "name": "Snowboarding Jacket", "description": "A description for this item" },
        { "name": "Snowboard", "description": "A description for this item" },
    ]
})
category_items.append({
    "category": "Soccer",
    "items": [
        { "name": "Soccer Ball", "description": "A description for this item" },
        { "name": "Soccer Gloves", "description": "A description for this item" },
        { "name": "Soccer Goal Post", "description": "A description for this item" },
        { "name": "Soccer Shin Guards", "description": "A description for this item" },
        { "name": "Soccer Uniform", "description": "A description for this item" },
    ]
})
category_items.append({
    "category": "Tennis",
    "items": [
        { "name": "Tennis Balls (3-pack)", "description": "A description for this item" },
        { "name": "Tennis Hat", "description": "A description for this item" },
        { "name": "Tennis Headband", "description": "A description for this item" },
        { "name": "Tennis Racket", "description": "A description for this item" },
        { "name": "Tennis Shirt (black)", "description": "A description for this item" },
        { "name": "Tennis Shirt (white)", "description": "A description for this item" },
    ]
})

for x in category_items:
    category = Category(name = x['category'])
    session.add(category)
    session.commit()

    for y in x['items']:
        item = Item(name = y['name'], category = category, description = y['description'])
        session.add(item)
        session.commit()
