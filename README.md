# Description
SPARQL query log collection and analysis:
* SPARQL canonicalisation/normalization is done using [QCan library](https://github.com/RittoShadow/QCan)
* Template discovery is done with the ISWC paper: [How is your Knowledge Graph Used:
Content-Centric Analysis of SPARQL Query
Logs](https://iswc2023.semanticweb.org/wp-content/uploads/2023/11/142650191.pdf%E2%80%9D)

# Structure
```python
/log_analysis    # source code for collecting sparql queries from the GLACIATION platform
 /logs/eda.ipynb # contains Jyputer notebook for analysing results, e.g., calculating entropy of discovered templates of queries
/resultFiles     # used by QCan library
main.py          # entry point for running canonicalisation -> discovering templates for each sparql queries
requirements.txt # required libraries dumped by ```pip freeze > requirements.txt```
```

# Example
Step 1: Execute the QCan and template discovery: 

```$ python -m main```

This step will generate two files: ```T_generalized``` and ```T_specialized``` under ```/log_analysis/logs```

Step 2: Analyze the generated templates 

```$ jupyter notebook ```

Now we can open ```/log_analysis/logs/eda.ipynb``` Jupyter notebook for analyzing the results (see the notebook for details)
