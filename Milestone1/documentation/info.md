## Data Collection

We collected raw data from two big datasets, one being the Kindle Store products and the other being the Kindle Store products reviews.

The Kindle Store Products dataset has the data divided into the following aspects:


```
    asin - ID of the product, e.g. 0000031852
    title - name of the product
    feature - bullet-point format features of the product
    description - description of the product
    price - price in US dollars (at time of crawl)
    imageURL - url of the product image
    imageURL - url of the high resolution product image
    related - related products (also bought, also viewed, bought together, buy after viewing)
    salesRank - sales rank information
    brand - brand name
    categories - list of categories the product belongs to
    tech1 - the first technical detail table of the product
    tech2 - the second technical detail table of the product
    similar - similar product table
```
The kindle store reviews dataset has the data divided into the following aspects:

```
    reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
    asin - ID of the product, e.g. 0000013714
    reviewerName - name of the reviewer
    vote - helpfull votes of the review
    reviewText - text of the review
    overall - rating of the product
    summary - summary of the review
    unixReviewTime - time of the review (unix time)
    reviewTime - time of the review (raw)
    image - images that users post after they have received the product
```


## Data Preparation

We shall use these attributes because:

- asin - we need this to connect to the reviews table
- title -for data retrieval purposes
- feature - help in data categorization
- descritpion - help in data categorization
- imageURL - possible need in the retrieval system
- brand - for data retrieval purposes
  
- reviewerID - for query purposes
- reviewerName - for data retrieval purposes
- vote - query results filtering and sorting
- reviewText - data retrieval purposes
- overall -  query results filtering and sorting
- summary - data retrieval purposes
- unixReviewTime - query results filtering and sorting
- reviewTime - time of the review (raw)