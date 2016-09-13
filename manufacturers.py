import helpers as h

def get_manufacturer(p):
    return p.get("manufacturer", "No field")

h.count_values('data/products.txt', get_manufacturer)
