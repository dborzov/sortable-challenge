def extract_tokens(label):
    tokens = [t for t in label.replace('-',' ').split()]
    return tokens

def generate_variants(tokens):
    separators = [" ", "-", "", "_"]
    return set([sep.join(tokens) for sep in separators])
