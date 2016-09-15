from decision_tree import root, listings, json, UnRecognizedListing

i = 0
for listing in listings:
    i += 1
    if i>30:
        break
    with open("tmp/{}.txt".format(str(i)),"w") as log:
        log.write(json.dumps(listing))
        try:
            rr = root.apply(listing)
            log.write("\nClassified!\n \n")
            log.write(rr)
        except UnRecognizedListing as e:
            log.write("Not recognized!\n \n")
            log.write(e.__str__())
