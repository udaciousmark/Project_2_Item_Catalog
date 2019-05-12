#!/usr/bin/env python2

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

DB_NAME = 'catalog'
app = Flask(__name__)

engine = create_engine('postgresql+psycopg2:///' + DB_NAME)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def index():
    categories = session.query(Category).all()
    num_latest_items = 10
    latest_items = session.query(Item, Category)\
                          .join(Category, Item.category_id==Category.id)\
                          .order_by(desc(Item.id))\
                          .limit(num_latest_items)\
                          .all()
    return render_template('index.html',
                           categories=categories,
                           latest_items=latest_items)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
