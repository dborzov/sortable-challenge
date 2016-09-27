My take at Sortable's listing matching challenge.

# Running the script
The script is written in Python 2.7 which tends to be available on most Linux distributions by default (on MacOSX too). Please refer to, for example, instructions [here](http://docs.python-guide.org/en/latest/) for details on how to install Python if it is not. No packages outside of the standard library are used so all that is needed  in most cases is to clone the repo.

To run it, clone the repo, `cd` into the repo's directory and run:
```
python solution.py  [OPTIONS]
```
The supported options enable customizing the file locations that will be used:
```
-p <path-to-products-file>, <pwd>/products.txt path is used if not specified
-l <path-to-listings-file>, <pwd>/listings.txt path is used if not specified
-r <path-to-output-results-file>, <pwd>/results.jsonl path is used if not specified
```
The results are written to a JSONL file as specified. The script also outputs (to STDERR) short progress messages during execution and a short summary at the end:
```
743 products parsed, the classifying_tree is built!
processing listings... 20196 processed, 7599 identified
 Done!
   *  processed 743 products
   * 20196 listings
   *  of those identified 7599 listings
```

The products with no matching listings are not included in the results file.

# Overview
Here is the summary of the approach the script uses.

First, it uses the products dataset to build a search tree data structure we would refer to as `classifying_tree`.

Then it applies that `classifying_tree`'s search method to each listing to see if there is a product match for it.

Each node of the `classifying_tree` has a unique `match` function that is applied to a listing and returns a boolean indicating whether there is a   match.      

When a listing reaches a `classifying_tree` node, there are two possibilities:

* If it is a tree leaf and it has the product attached to it, that means the search succeeded and that product is returned as the classification result for that listing;  
* Otherwise, it is checked for a match against all the children of that node. If there is one match, the listing traverses down the tree to that node. If there is none or several matches, that means the search failed and no products are matched to that listing. The reason we toss out the listings that get several matches is we treat this ambiguity

Each product's tree node keeps track of the listings it was matched to. After going through all the listings, we traverse the tree to print out the list of products along with the listings it was matched to and output it as JSONL.

## Structure of the classifying tree
Here is a diagram:

```
Root -> Manufacturer matchers ->     Family matchers -> Models
  |
  |--- Sony ----------------------|- No family -------- M300
  |                               |- Cybershot -------- S30
  |
  |--- Canon-----------------------No family |
                                             |-------- F40
                                             |-------- F50
```
We see that root's children nodes are manufacturer matchers. That is, first, we attempt to identify a manufacturer in a listing.

Once the manufacturer is identified, we try to identify the listing's family. That is, each `ManufacturerNode` of the tree has family matchers as it's children (`FamilyNode` nodes).

There is a special `FamilyNode` for products with undefined family field value (we will refer to it as a `NoFamilyNode` here). The manufacturer's matching method thus is a bit different from the other node's matching procedure: if no family value was matched and `NoFamilyNode` is not empty (that is, has some product leave nodes), we traverse down to that node instead of declaring the search failed.

Once on the family level, we get down to identifying individual models.

Here are some features of the node's behavior:

* There are some special cases for manufacturer matchers that take into account things like *HP* being the same thing as *Hewlett-Packard* or *Konica* being now the same thing as *Minolta*.
* When a product is added to the tree, we check for collisions on each level (Manufacturer, Family, Model) using the same search method we apply to listings. That lets us identify attempting to add one product several times and avoid matching collisions on each level.

## Tests
The script comes with two sets of tests:

* `test` directory contains the **functional tests**. That usually includes the algorithm being applied to one-two products and listings to assure some specific behaviour

* `classifying_tree/test_*.py` contain some **unit tests**

To run the tests use:
```
python -m unittest discover -v
```

# The process used
The general outline was this:

* **Data Exploration**: the first and the crucial stage is to look at the given sample dataset, go through several examples "by hand" and try learning about the character of the problem as much as we can
* **Deciding on the approach**: We then attempt to formalize what we learned and come up with an approach appropriate for the given problem
* **Implementation**: We write the code and unit-test its components to make sure all the parts behave as intended
* **Documenting**: At last, we document what we did and why

# Data exploration observations
Below are some observations from my data exploration this solution was built upon.

## Not a good problem for probabilistic approaches
The following two constraints:
* The primary specified requirement in the problem statement is to minimize the number of wrong matches (as opposed to, say, have the largest possible number of correct matches)
* The space of the classification outcomes for each individual listing is vast: in our case it can be any of almost a thousand of the provided product entries (as opposed to, say, a yes/no type of classification problem)

That mean that this is not a good problem to tackle with any kind of probabilistic or fitness function maximization-based approach. Instead, we will focus on identifying a set of yes/no criteria for each product that would be able to reasonably identify the listing as belonging to that product.


## Model and family are a weak identifiers for products
While the pair of `family`/`model` field values is unique for all the product entries within the given dataset, looking at them in detail shows that the value collisions are very much a possibility.

For example, the model values can be identical:
```
700 (manufacturer: Epson| family: PhotoPC)
700 (manufacturer: Fujifilm| family: FinePix)
700 (manufacturer: Nikon| family: Coolpix)
```
and even when they are not, they can be hard to distinguish:
```
100 (manufacturer: Nikon| family: Coolpix)
100 HS (manufacturer: Canon| family: ELPH)
```


## An overlap between family and model fields for products
While it seems that the intention was for the `family` field to refer to the series of the product and for the model to identify individual models within the family, we see that the provided products dataset does not quite adhere to that distinction.

For example, for Leica models, one product's `family` name colliding with another product's `model` name:
```
manufacturer: Leica, family: NONE, model: Digilux
manufacturer: Leica, family:Digilux, model: 4.3
```
Common sense suggests that in cases like this, `Digilux` is the appropriate name for the series of products and here the entry with `Digilux` as a `model` value should be ignored.

## Different separators used interchangeably
For model and family values, the following different separators are perceived as identical by humans:
* One word(e.g. Sony Cybershot)
* Camelcase(e.g. Sony CyberShot)
* Dashed (e.g. Sony Cyber-shot)
* With a space (e.g. Sony Cyber shot)
* With an underscore (e.g. Cyber_shot)

The code accounts for it by recognizing those separators, using them to split the string into "tokens", and matching only those (we are using regex expressions for that).
