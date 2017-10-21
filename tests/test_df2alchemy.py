import pandas as pd
from df2sqlalchemy import load_model_from_dataframe
import unittest

from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

import os
import sqlite3

class TestDf2SqlAlchemy(unittest.TestCase):
    def setUp(self):
        data = [
                ["Foo", 37, 10.3],
                ["Bar", 123, 9.3]
                ]

        columns = ["name", "count", "price"]

        self.df = pd.DataFrame(data, columns=columns)

    def test_convert(self):
        model = load_model_from_dataframe('books', self.df, primary_keys=['name'])
        self.assertIsInstance(model, sqlalchemy.Table)

        self.assertIsInstance(model.columns['name'].type, sqlalchemy.String)
        self.assertIsInstance(model.columns['count'].type, sqlalchemy.Integer)
        self.assertIsInstance(model.columns['price'].type, sqlalchemy.Float)

        self.assertEqual(model.name, "books")
        self.assertEqual(model.primary_key.columns.keys(), ['name'])

    def test_map(self):
        type_map = { 'name': sqlalchemy.Text}
        model = load_model_from_dataframe('books', self.df, primary_keys=['name'], type_map=type_map)
        self.assertIsInstance(model.columns['name'].type, sqlalchemy.Text)

    def test_integration(self):
        model = load_model_from_dataframe('books', self.df, primary_keys=['name'])
        db_file = 'test.sqlite'
        try:
            db_path = 'sqlite:///%s'%db_file
            engine = create_engine(db_path)
            model.metadata.create_all(engine)

            with sqlite3.connect(db_file) as conn:
                conn.cursor().execute("SELECT name, count, price FROM books")

        except Exception as e:
            self.fail("%s raised"%e)
        finally:
            os.remove(db_file)


