#!/usr/bin/env python2

from flask import Flask, jsonify, redirect, render_template, request, url_for
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


@app.route('/catalog/<string:category_name>/items')
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


@app.route('/catalog/<string:category_name>/<string:item_name>')
def item(category_name, item_name):
    category = session.query(Category)\
                      .filter_by(name=category_name)\
                      .one()
    item = session.query(Item)\
                  .filter_by(category_id=category.id)\
                  .filter_by(name=item_name)\
                  .one()
    return render_template('item.html', category=category, item=item)


@app.route('/catalog/new_item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        item_name=request.form['item_name']
        item_description=request.form['item_description']
        category_name = request.form['category_name']

        category = session.query(Category)\
                          .filter_by(name=category_name)\
                          .first()

        # If category doesn't exist, then we need to create category & item
        if category is None:
            category = Category(name=category_name)
            session.add(category)
            session.commit()

            new_item = Item(name=item_name, description=item_description, category_id=category.id)
            session.add(new_item)
            session.commit()

            return redirect(url_for('category_items', category_name=category_name))

        item = session.query(Item)\
                      .filter_by(name=item_name)\
                      .filter_by(category_id=category.id)\
                      .first()

        # If item name already exists in this category
        if item is not None:
            return redirect(url_for('new_item', category_name=category_name))

        new_item = Item(name=item_name, description=item_description, category_id=category.id)
        session.add(new_item)
        session.commit()

        return redirect(url_for('category_items', category_name=category_name))
    else:
        return render_template('new_item.html')


@app.route('/catalog/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(category_name, item_name):

    if request.method == 'POST':
        original_category_name = category_name
        original_category = session.query(Category)\
                                   .filter_by(name=original_category_name)\
                                   .one()
        item = session.query(Item)\
                      .filter_by(name=item_name)\
                      .filter_by(category_id=original_category.id)\
                      .first()

        new_category_name = request.form['category_name']
        new_category = session.query(Category)\
                          .filter_by(name=new_category_name)\
                          .first()
        if new_category is None:
            new_category = Category(name=new_category_name)
            session.add(new_category)
            session.commit()

        item.name = request.form['item_name']
        item.description = request.form['item_description']
        item.category_id = new_category.id

        session.add(item)
        session.commit()

        return redirect(url_for('category_items', category_name=new_category.name))
    else:
        category = session.query(Category)\
                          .filter_by(name=category_name)\
                          .one()
        item = session.query(Item)\
                      .filter_by(category_id=category.id)\
                      .filter_by(name=item_name)\
                      .one()

        return render_template('edit_item.html', category=category, item=item)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    category = session.query(Category)\
                      .filter_by(name=category_name)\
                      .one()
    item_to_delete = session.query(Item)\
                            .filter_by(category_id=category.id)\
                            .filter_by(name=item_name)\
                            .one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        return redirect(url_for('category_items', category_name=category.name))
    else:
        return render_template('delete_item.html', category=category, item=item_to_delete)


@app.route('/catalog.json')
def catalog_json():
    all_categories = session.query(Category).all()
    catalog = {"categories": []}

    for category in all_categories:
        items = session.query(Item)\
                       .filter_by(category_id=category.id)\
                       .all()
        category_json = category.serialize
        category_json.update(items=[i.serialize for i in items])
        catalog['categories'].append(category_json)
    return jsonify(catalog=catalog)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
