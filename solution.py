from classifying_tree import JSONL, tree, add_product, UnrecognizedListing
import sys, getopt, json

# parse cli arguments for options
jsonl_path_products = './data/products.txt'
jsonl_path_listings = './data/listings.txt'
jsonl_path_results = 'results.jsonl'
opts, _ = getopt.getopt(sys.argv[1:],"p:l:r:", ["products=","listings=","results="])
for opt, val in opts:
    if opt in ["-p", "--products"]:
        jsonl_path_products = val
    if opt in ["-l", "--listings"]:
        jsonl_path_listings = val
    if opt in ["-r", "--results"]:
        jsonl_path_results = val


# we will log progress to stderr by default
log = sys.stderr

# parse products file and add products to the classyfying tree
count_products = 0
log.write('parsing products...')
for product in JSONL(jsonl_path_products):
    log.write('\rparsing products... {} parsed'.format(count_products))
    count_products += 1
    add_product(tree, product)
log.write('\r{count_products} products parsed, the classifying_tree is built!\n'.format(**locals()))

# search for each listing with the classifying_tree
count_listings, count_identified = 0, 0
for listing in JSONL(jsonl_path_listings):
    count_listings += 1
    log.write('\rprocessing listings... {} processed, {} identified'.format(count_listings, count_identified))
    try:
        cur = tree.search(listing)
        count_identified += 1
    except UnrecognizedListing as e:
        continue

# write results into a file by traversing the classifying tree
with open(jsonl_path_results,"w") as result_file:
    tree.write_result(result_file)

# log what was done
SUMMARY_MESSAGE = """
\r Done!
   *  processed {count_products} products
   * {count_listings} listings
   *  of those identified {count_identified} listings
"""
log.write(SUMMARY_MESSAGE.format(**locals()))
