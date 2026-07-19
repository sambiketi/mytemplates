


from app import db
from app.models.product import Product
from datetime import datetime

class ProductService:
    @staticmethod
    def get_all():
        return Product.query.filter_by(is_active=True).all()
    
    @staticmethod
    def get_featured(limit=4):
        return Product.query.filter_by(is_active=True, is_featured=True).limit(limit).all()
    
    @staticmethod
    def get_by_category(category):
        return Product.query.filter_by(category=category, is_active=True).all()
    
    @staticmethod
    def get_by_slug(slug):
        return Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    @staticmethod
    def get_related(product, limit=3):
        return Product.query.filter_by(category=product.category, is_active=True).filter(Product.id != product.id).limit(limit).all()
    
    @staticmethod
    def create(data):
        product = Product(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            category=data['category'],
            image_url=data.get('image_url'),
            action_link=data.get('action_link')
        )
        db.session.add(product)
        db.session.commit()
        return product
    
    @staticmethod
    def update(product, data):
        product.title = data.get('title', product.title)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.category = data.get('category', product.category)
        product.image_url = data.get('image_url', product.image_url)
        product.action_link = data.get('action_link', product.action_link)
        db.session.commit()
        return product
    
    @staticmethod
    def delete(product):
        db.session.delete(product)
        db.session.commit()
    
    @staticmethod
    def get_categories():
        return db.session.query(Product.category).filter_by(is_active=True).distinct().all()




