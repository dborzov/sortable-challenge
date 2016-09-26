import re

def extract_tokens(label):
    tokenized_camel_cases = " ".join([t.lower() for t in re.split('(\B[A-Z][a-z]*)', label) if not len(t)==0])
    tokenized_numerics = " ".join([t.lower() for t in re.split('([1-9]+)', tokenized_camel_cases) if not len(t)==0])
    tokens = [t for t in tokenized_numerics.replace('-',' ').split()]
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

def label2regex(label):
    return tokens2regex(extract_tokens(label))

def tokens2regex(tokens):
    return "[-\s]*".join(tokens)
