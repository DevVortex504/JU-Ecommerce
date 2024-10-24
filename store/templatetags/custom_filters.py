from django import template

register = template.Library()

@register.filter
def calculate_discount(price, discounted_price):
    if price and discounted_price:
        discount = (float(price) - float(discounted_price)) / float(price) * 100
        return round(discount)
    return 0