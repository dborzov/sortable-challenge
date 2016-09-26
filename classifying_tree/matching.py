import re

def extract_tokens(label):
    de_camel_cased = " ".join([t.lower() for t in re.split('(\B[A-Z][a-z]*)', label) if not len(t)==0])
    tokens = [t for t in de_camel_cased.replace('-',' ').split()]
    return tokens

SEPARATORS = [" ", "-", "", "_"]
def generate_variants(tokens):
    if len(tokens) <= 1:
        return tokens
    variants = set()
    for subvariant in generate_variants(tokens[1:]):
        for sep in SEPARATORS:
            variants.add(tokens[0]+sep+subvariant)
    return variants
