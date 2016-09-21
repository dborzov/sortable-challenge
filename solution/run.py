from build import *

i=0
for listing in listings:
    i += 1
    # if i>3000:
    #     break
    with open("tmp/{}.txt".format(str(i)),"w") as log:
        log.write(json.dumps(listing))
        try:
            rr = decision_tree.search(listing)
            log.write("\nClassified!\n \n")
            cur = rr
            while True:
                cur.listing_counter += 1
                log.write(cur.label)

                cur = cur.parent
                if cur is None:
                    break
        except UnrecognizedListing as e:
            log.write("Not recognized!\n \n")
            log.write(e.__str__())

decision_tree.traverse()
