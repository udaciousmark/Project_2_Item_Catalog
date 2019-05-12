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
    all_categories = session.query(Category).all()
    num_latest_items = 10
    latest_items = session.query(Item, Category)\
                          .join(Category, Item.category_id == Category.id)\
                          .order_by(desc(Item.id))\
                          .limit(num_latest_items)\
                          .all()
    return render_template('index.html',
                           all_categories=all_categories,
                           latest_items=latest_items)


@app.route('/<string:category_name>/items')
def category_items(category_name):
    all_categories = session.query(Category).all()
    category = session.query(Category)\
                      .filter_by(name=category_name)\
                      .one()
    category_items = session.query(Item)\
                            .filter_by(category_id=category.id)\
                            .order_by(Item.name)\
                            .all()
    return render_template('category_items.html',
                           all_categories=all_categories,
                           category=category,
                           category_items=category_items)


@app.route('/<string:category_name>/<string:item_name>')
def item(category_name, item_name):
    category = session.query(Category)\
                      .filter_by(name=category_name)\
                      .one()
    item = session.query(Item)\
                  .filter_by(category_id=category.id)\
                  .filter_by(name=item_name)\
                  .one()
    return render_template('item.html', item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
