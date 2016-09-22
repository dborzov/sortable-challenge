from build import *
import sys
count_listings = 0
count_identified = 0

sys.stderr.write('starting processing listings...')
for listing in listings:
    count_listings += 1
    sys.stderr.write('\rprocessing... {} processed, {} identified'.format(count_listings, count_identified))
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

decision_tree.traverse()
