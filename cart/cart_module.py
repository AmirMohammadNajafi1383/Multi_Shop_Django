
from product.models import Product

CART_SESSION_KEY = 'cart'
class Cart:
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY, )
        if not cart:
            cart =  self.session[CART_SESSION_KEY]={}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()

        for item in cart.values():
            # Check if the 'id' key is present in the item dictionary


                    product = Product.objects.get(id=item['id'])
                    item['product'] = product
                    item['total'] = int(item['quantity']) * int(item['price'])


                    yield item


    def unique_id_generator(self,id,quantity,color,size):
        result = f'{id}-{quantity}-{color}-{size}'
        return result

    def add(self,id,product,quantity,color,size):
        unique = self.unique_id_generator(id,quantity,color,size)
        if unique not in self.cart:
            self.cart[unique] = {'quantity':0,'price':str(product.price),'color':color,'size':size,'name_unique':unique,'id':id}

        self.cart[unique]['quantity'] += int(quantity)

        self.save()

    def total(self):
        cart = self.cart.values()
        total= sum(int(item['price']) * int(item['quantity']) for item in cart)
        return total

    def remove_cart(self):
        del self.session[CART_SESSION_KEY]
    def delete(self,id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True
