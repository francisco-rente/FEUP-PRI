"""
Run this file from this folder (python3 eval_query.py) and not from root or
  other folder (python3 scripts/eval_query.py)
The query file path is relative to the scripts source
The queries that are made in a subset of the data are made in a different core
"""





import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
# import json
import requests
import pandas as pd
import pickle
from itertools import cycle



QRELS_FILE = [
    "query_qrel/query1.txt",
    "query_qrel/query2.txt", 
    "query_qrel/query3.txt",
    "query_qrel/query4.txt"
    
]
queries =[ 
    (1, "http://localhost:8983/solr/kindle/select?indent=true&q.op=OR&q=brand%3A%20Francis&rows=10&sort=overall%20desc"), #query 1
    (2, "http://localhost:8983/solr/kindle/select?defType=dismax&fq=no_pages%3A%5B0%20TO%20150%5D&indent=true&q.op=OR&q=soccer%20football&qf=title%20brand%20description&sort=no_pages%20asc"), #query 2
    (3, "http://localhost:8983/solr/kindle/select?defType=edismax&fq=%7B!join%20from%3Did%20to%3Dasin%7Dbrand%3A%22Dr.%20Leland%20Benton%22&fq=overall%3A%5B4.0%20TO%20*%5D&indent=true&q.op=OR&q=good&qf=reviewText%20%20summary&qs=1&rows=20&sort=visualization%20desc%20%2Chelpful_ratio%20desc"), #query 3
    (4, "http://localhost:8983/solr/sampled_kindle/select?defType=edismax&fq=type%3A%22review%22%20reviewTime%3A%5B2013-6-1T00%3A00%3A00Z%20TO%202013-8-31T00%3A00%3A00Z%5D&indent=true&q.op=OR&q=%22vacation%20read%22&qf=reviewText%20%20summary&qs=1&rows=12&sort=helpful_ratio%20desc%2C%20visualization%20desc"), #query 4
]

queries_boosted = [
    (1, "http://localhost:8983/solr/kindle/select?indent=true&q.op=OR&q=brand%3A%20Francis&rows=10&sort=overall%20desc"), #query 1
    (2, "http://localhost:8983/solr/sampled_kindle/select?defType=dismax&fq=no_pages%3A%5B0%20TO%20150%5D&indent=true&q.op=OR&q=soccer%20football&qf=title%5E2%20brand%20description&sort=no_pages%20asc"), #query 2
    (3, "http://localhost:8983/solr/kindle/select?defType=edismax&fq=%7B!join%20from%3Did%20to%3Dasin%7Dbrand%3A%22Dr.%20Leland%20Benton%22&fq=overall%3A%5B4.0%20TO%20*%5D&indent=true&q.op=OR&q=good&qf=reviewText%5E1%20%20summary%5E2&qs=1&rows=10&sort=visualization%20desc%20%2Chelpful_ratio%20desc"), #query 3
    (4, "http://localhost:8983/solr/sampled_kindle/select?defType=edismax&fq=type%3A%22review%22%20reviewTime%3A%5B2013-6-1T00%3A00%3A00Z%20TO%202013-8-31T00%3A00%3A00Z%5D&indent=true&q.op=OR&q=%22vacation%20read%22&qf=reviewText%5E1.3%20%20summary%5E1.7&qs=1&rows=12&sort=helpful_ratio%20desc%2C%20visualization%20desc"), #query 4
]





SCHEMA = 1  # 1 if using schema, 0 if filterless, -1 if creating graphs

# Guardar vars de schema e schema_boost numa só run
# correr sem schema (necessário reboot de docker) e guardar vars
# fazer gráficos


def process_query(index: int, q_type: str, query_file: str, query_url: str):
    # Read qrels to extract relevant documents
    relevant = list(map(lambda el: el.strip(), open(query_file).readlines()))
    # Get query results from Solr instance
    results = requests.get(query_url).json()['response']['docs']


    # METRICS TABLE
    # Define custom decorator to automatically calculate metric based on key
    metrics = {}
    def metric(f): metrics.setdefault(f.__name__, f)
    # metric = lambda f: metrics.setdefault(f.__name__, f)

    @metric
    def ap(results, relevant):
        """Average Precision"""
        relevant_index = []
        index = 0
        for res in results:
            if (i != 0 and res['id'] in relevant) or (i == 0 and res['id'][0] in relevant):
                relevant_index.append(index)
            index = index + 1

        if len(relevant_index) == 0:
            return 0

        precision_values = [
            len([
                doc
                for doc in results[:idx]
                if (i != 0 and doc['id'] in relevant) or (i == 0 and doc['id'][0] in relevant)
            ]) / idx
            for idx in range(1, len(results) + 1)
        ]
        
        precision_sum = 0
        for ind in relevant_index:
            precision_sum = precision_sum + precision_values[ind]

        return precision_sum/len(relevant_index)

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
    df = pd.DataFrame([['Metric', 'Value']] + [
            [evaluation_metrics[m], calculate_metric(m, results, relevant)]
            for m in evaluation_metrics
        ]
    )

    with open(f'results/{q_type}_results_{index}.tex', 'w') as tf:
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

    # If could not find any value
    if not precision_values and not recall_values:
        precision_values = [0]
        recall_values = [0]

    precision_recall_match = {k: v for k, v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(0, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            print(step)
            if idx > 0 and recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+2]]

    disp = PrecisionRecallDisplay(precision=[precision_recall_match.get(r) for r in recall_values], recall=recall_values)
    disp.plot()
    plt.savefig(f'results/{q_type}_precision_recall_{index}.png')

    return disp


try:
    with open('data.pickle', 'rb') as file:
        values_dict = pickle.load(file)
except FileNotFoundError:
    print("Didn't find saved plots, creating new dict")
    values_dict = {
        "filterless": {1: None, 2: None, 3: None, 4: None, 5: None},
        "schema": {1: None, 2: None, 3: None, 4: None, 5: None},
        "schema_boost": {1: None, 2: None, 3: None, 4: None, 5: None},
    }

if SCHEMA == 1:
    for index in range(0, len(queries)):
        i, link = queries[index]
        print(f"Handling query nº{i} with schema without boosts")
        disp = process_query(i, 'schema', QRELS_FILE[index], link)
        values_dict['schema'][i] = disp

        i, link = queries_boosted[index]
        print(f"Handling query nº{i} with schema with boosts")
        disp = process_query(i, 'schema_boost', QRELS_FILE[index], link)
        values_dict['schema_boost'][i] = disp

        with open('data.pickle', 'wb') as file:
            pickle.dump(values_dict, file)
            
elif SCHEMA == 0:
    for index in range(0, len(queries)):
        i, link = queries[index]
        print(f"Handling query nº{i} without schema ")
        disp = process_query(i, 'filterless', QRELS_FILE[index], link)
        values_dict['filterless'][i] = disp

        with open('data.pickle', 'wb') as file:
            pickle.dump(values_dict, file)
elif SCHEMA == -1:
    colors = cycle(["navy", "turquoise", "darkorange"])
    _, ax = plt.subplots(figsize=(7, 8))
    for i in range(1, len(queries)+1):
        values_dict['filterless'][i].plot(ax=ax, name=f"Precision-recall for filterless query {i}", color=next(colors))
        values_dict['schema'][i].plot(ax=ax, name=f"Precision-recall for schema query {i}", color=next(colors))
        values_dict['schema_boost'][i].plot(ax=ax, name=f"Precision-recall for schema_boost query {i}", color=next(colors))
        #draw plot in svg format
        plt.savefig(f'results/all_precision_recall_{i}.png')
        plt.cla()


# for i, d in enumerate(disps):
#     d.plot(ax=ax, name=f"Precision-recall for query {i}", color=next(colors))

# plt.show()