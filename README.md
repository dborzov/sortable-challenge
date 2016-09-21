My take at Sortable's listing matching challenge.

# The solution
The script is written in Python 2.7 which should be available on most Linux and MacOSX machines by default.

To execute it, clone the repo and run:
```
python solution.py  <path-to-products-file> <path-to-products-file>
```

### The algorithm
Here is what the script does.

First, it uses the products dataset to build a search tree data structure we would refer to as `decision_tree`.

Then it applies that `decision_tree`'s search method to each listing to see if there is a product match for it.

Each node of the `decision_tree` has a unique `match` function that is applied to a listing and returns a boolean indicating whether there is a   match.      

When a listing reaches a `decision_tree` node, there are two possibilities:

* If it is a tree leaf and it has the product attached to it, that means the search succeeded and that product is returned as the classification result for that listing;  
* Otherwise, it is checked for a match against all the children of that node. If there is one match, the listing traverses down the tree to that node. If there is none or several matches, that means the search failed and no products are matched to that listing.

# The process
This section describes my reasoning and thought process of arriving at the given solution.

The general outline is this:

* **Data Exploration**: the first and the crucial stage is to look at the given sample dataset, go through several examples "by hand" and try learning about the character of the problem as much as we can
* **Deciding on the approach**: We then attempt to formalize what we learned and come up with an approach appropriate for the given problem
* **Implementation**: We write the code and unit-test its components to make sure all the parts behave as intended
* At last, we document what we did and why

### Stage 1: Data exploration
We look at the given datasets. Below are some observations worth highlighting.

##### Model and family are a weak identifiers for products
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

##### An overlap between family and model fields for products
While it seems that the intention was for the `family` field to refer to the series of the product and for the model to identify individual models within the family, we see that the provided products dataset does not quite adhere to that distinction.

For example, for Leica models, one product's `family` name colliding with another product's `model` name:
```
manufacturer: Leica, family: NONE, model: Digilux
manufacturer: Leica, family:Digilux, model: 4.3
```
Common sense suggests that in cases like this, `Digilux` is the appropriate name for the series of products and here the entry with `Digilux` as a `model` value should be ignored.

### Stage 2: Deciding on the approach
The following two constraints:
* The primary specified requirement in the problem statement is to minimize the number of wrong matches (as opposed to, say, have the largest possible number of correct matches)
* The space of the classification outcomes for each individual listing is vast: in our case it can be any of almost a thousand of the provided product entries (as opposed to, say, a yes/no type of classification problem)

That mean that this is not a good problem to tackle with any kind of probabilistic or fitness function maximization-based approach. Instead, we will focus on identifying a set of yes/no criteria for each product that would be able to reasonably identify the listing as belonging to that product.         

### Stage 3: Implementation
