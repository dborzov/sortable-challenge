import re

def extract_tokens(label):
    de_camel_cased = " ".join([t.lower() for t in re.split('(\B[A-Z][a-z]+)', label) if not len(t)==0])
    tokens = [t for t in de_camel_cased.replace('-',' ').split()]
    return tokens

def generate_variants(tokens):
    separators = [" ", "-", "", "_"]
    return set([sep.join(tokens) for sep in separators])
