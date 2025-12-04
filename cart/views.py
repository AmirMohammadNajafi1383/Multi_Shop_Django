from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import Http404,HttpResponse


from cart.cart_module import Cart
from cart.models import Order, OrderItem, DiscountCode
from product.models import Product


class CartDetailView(LoginRequiredMixin,View):
    def get(self, request, **kwargs):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        color, size, quantity = request.POST.get('color', 'empty'), request.POST.get('size', 'empty'), request.POST.get(
            'quantity', )
        cart = Cart(request)
        cart.add(pk, product, quantity, color, size)
        return redirect('cart:cart_detail')


class OrderDetailView(LoginRequiredMixin,View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/order_detail.html', {'order': order})


class OrderCreateView(LoginRequiredMixin,View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=self.request.user, total_price=cart.total())
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product']
                                     , quantity=item['quantity'], color=item['color'], size=item['size'],
                                     price=int(item['price']))

        cart.remove_cart()
        return redirect('cart:order_detail',order.id)




class DiscountView(LoginRequiredMixin,View):
    def post(self, request, pk):
        try:
            code = request.POST.get('discount_code')
            order = get_object_or_404(Order, id=pk)
            discount_code = get_object_or_404(DiscountCode, name=code)

            if discount_code.quantity == 0:
                return redirect('cart:order_detail', order.id)

            discount_amount = order.total_price * discount_code.percent_discount / 100
            if discount_amount > order.total_price:
                discount_amount = order.total_price  # Ensure discount doesn't exceed total price

            order.total_price -= discount_amount
            order.save()

            discount_code.quantity -= 1
            discount_code.save()

            return redirect('cart:order_detail', order.id)

        except Order.DoesNotExist:
            raise Http404("Order does not exist")

        except DiscountCode.DoesNotExist:
            return HttpResponse("Invalid discount code")
