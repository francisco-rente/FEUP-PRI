# SETUP
# This script is used to evaluate the performance of the search engine

#This scripts should be used from the Milestone 2 folder

import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd


QRELS_FILE = [
    "query_qrel/query3.txt",
    "query_qrel/query4.txt"
]
QUERY_URL = [
    "", #query 1
    "", #query 2
    "http://localhost:8983/solr/#/kindle/query?q=good&q.op=OR&defType=edismax&indent=true&qf=reviewText%20%20summary&qs=1&sort=visualization%20desc%20,helpful_ratio%20desc&rows=20&fq=%7B!join%20from%3Did%20to%3Dasin%7Dbrand:%22Dr.%20Leland%20Benton%22&fq=overall:%5B4.0%20TO%20*%5D", #query 3
    "http://localhost:8983/solr/#/kindle/query?q=%22vacation%20read%22&q.op=OR&defType=edismax&indent=true&qf=reviewText%20summary&qs=1&sort=helpful_ratio%20desc,%20visualization%20desc&rows=20&fq=type:%22review%22%20reviewTime:%5B2013-6-1T00:00:00Z%20TO%202013-8-31T00:00:00Z%5D", #query 4
    "" #query 5
    
]

QUERY_URL_BOOSTED = [
    "", #query 1
    "", #query 2
    "http://localhost:8983/solr/#/kindle/query?q=good&q.op=OR&defType=edismax&indent=true&qf=reviewText%5E1.3%20%20summary%5E1.7&qs=1&sort=visualization%20desc%20,helpful_ratio%20desc&rows=20&fq=%7B!join%20from%3Did%20to%3Dasin%7Dbrand:%22Dr.%20Leland%20Benton%22&fq=overall:%5B4.0%20TO%20*%5D", #query 3
    "http://localhost:8983/solr/#/kindle/query?q=%22vacation%20read%22&q.op=OR&defType=edismax&indent=true&qf=reviewText%5E1.3%20%20summary%5E1.7&qs=1&sort=helpful_ratio%20desc,%20visualization%20desc&rows=20&fq=type:%22review%22%20reviewTime:%5B2013-6-1T00:00:00Z%20TO%202013-8-31T00:00:00Z%5D", #query 4
    "" #query 5
    
]
    

# Read qrels to extract relevant documents
relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
results = requests.get(QUERY_URL).json()['response']['docs']


# METRICS TABLE
# Define custom decorator to automatically calculate metric based on key
metrics = {}
metric = lambda f: metrics.setdefault(f.__name__, f)

@metric
def ap(results, relevant):
    """Average Precision"""
    precision_values = [
        len([
            doc 
            for doc in results[:idx]
            if doc['id'] in relevant
        ]) / idx 
        for idx in range(1, len(results))
    ]
    return sum(precision_values)/len(precision_values)

@metric
def p10(results, relevant, n=10):
    """Precision at N"""
    return len([doc for doc in results[:n] if doc['id'] in relevant])/n

def calculate_metric(key, results, relevant):
    return metrics[key](results, relevant)

# Define metrics to be calculated
evaluation_metrics = {
    'ap': 'Average Precision',
    'p10': 'Precision at 10 (P@10)'
}

# Calculate all metrics and export results as LaTeX table
df = pd.DataFrame([['Metric','Value']] +
    [
        [evaluation_metrics[m], calculate_metric(m, results, relevant)]
        for m in evaluation_metrics
    ]
)

with open('results.tex','w') as tf:
    tf.write(df.to_latex())




# PRECISION-RECALL CURVE
# Calculate precision and recall values as we move down the ranked list
precision_values = [
    len([
        doc 
        for doc in results[:idx]
        if doc['id'] in relevant
    ]) / idx 
    for idx, _ in enumerate(results, start=1)
]

recall_values = [
    len([
        doc for doc in results[:idx]
        if doc['id'] in relevant
    ]) / len(relevant)
    for idx, _ in enumerate(results, start=1)
]

precision_recall_match = {k: v for k,v in zip(recall_values, precision_values)}

# Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
recall_values.extend([step for step in np.arange(0.1, 1.1, 0.1) if step not in recall_values])
recall_values = sorted(set(recall_values))

# Extend matching dict to include these new intermediate steps
for idx, step in enumerate(recall_values):
    if step not in precision_recall_match:
        if recall_values[idx-1] in precision_recall_match:
            precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
        else:
            precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

disp = PrecisionRecallDisplay([precision_recall_match.get(r) for r in recall_values], recall_values)
disp.plot()
plt.savefig('precision_recall.pdf')
