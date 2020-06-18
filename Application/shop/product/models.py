from shop import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique = True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique = True)
    price = db.Column(db.Integer, nullable = False, unique = False)
    size = db.Column(db.Float, nullable = False, unique = False)
    add_info = db.Column(db.String(150), nullable = False, unique = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    category = db.relationship(Category, backref=db.backref('categories', lazy = True))
    image = db.Column(db.String(150), nullable = True)

    def __repr__(self):
        return '<Product %r>' % self.name
        
db.create_all()