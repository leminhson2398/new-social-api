from graphene import ObjectType, String, Int, Decimal, Boolean, Float


class ProductType(ObjectType):
    id = Int(required=True)
    title = String(required=True)
    slug = String(required=True)
    price = Decimal(required=True, default_value=0.0)
    description = String(required=True)
    stack = Int(required=True)
    available = Boolean(required=True, default_value=True)
    sale_percent = Decimal(required=True, default_value=0.0)
    weight = Float(required=True)
