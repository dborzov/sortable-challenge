import helpers as h

def get_manufacturer(p):
    if not p.get("manufacturer") == u"Sony":
        return "NOT SONY"
    return "SONY, " + p.get("family", "UNDEFINED FAMILY")

h.count_values('data/products.txt', get_manufacturer)
