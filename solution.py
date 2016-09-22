from solution.build import *
import sys

log = sys.stderr
count_listings = 0
count_identified = 0

log.write('starting processing listings...')
for listing in listings:
    count_listings += 1
    log.write('\rprocessing... {} processed, {} identified'.format(count_listings, count_identified))
    try:
        cur = decision_tree.search(listing)
        count_identified += 1
        while True:
            cur.listing_counter += 1
            cur = cur.parent
            if cur is None:
                break
    except UnrecognizedListing as e:
        continue

with open("results.jsonl","w") as result_file:
    decision_tree.write_result(result_file)
