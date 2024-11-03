from app.models.type import Type

class TypeService:
    @staticmethod
    def get_all_types():
        return Type.query.order_by(Type.name).all()

    @staticmethod
    def get_type_by_id(type_id):
        return Type.query.get(type_id)
    

from app.models.style import Style

class StyleService:
    @staticmethod
    def get_all_styles():
        return Style.query.order_by(Style.name).all()

    @staticmethod
    def get_style_by_id(style_id):
        return Style.query.get(style_id)