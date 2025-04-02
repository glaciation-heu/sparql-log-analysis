# Description
SPARQL query log collection and analysis:
* SPARQL canonicalisation/normalization is done using [QCan library](https://github.com/RittoShadow/QCan)
* Template discovery is done with the ISWC paper: [How is your Knowledge Graph Used:
Content-Centric Analysis of SPARQL Query
Logs](https://iswc2023.semanticweb.org/wp-content/uploads/2023/11/142650191.pdf%E2%80%9D)

# Structure
```python
📁log_analysis      # source code for collecting sparql queries from the GLACIATION platform
 📁logs
  📄eda.ipynb       # contains Jyputer notebook for analysing results, e.g., calculating entropy of discovered templates of queries
📁resultFiles       # used by QCan library
📄main.py           # entry point for running canonicalisation -> discovering templates for each sparql queries
📄cli.py            # command line interface for exploring SPARQL query templates and queries
📄requirements.txt  # required libraries dumped by ```pip freeze > requirements.txt```
```

# Example
**Step 1**: Execute the QCan and template discovery: 

```$ python -m main```

This step will generate two files: ```T_generalized``` and ```T_specialized``` under ```/log_analysis/logs```

**Step 2**: Analyze the generated templates 

```$ jupyter notebook ```

Now we can open ```/log_analysis/logs/eda.ipynb``` Jupyter notebook for analyzing the results (see the notebook for details)

# Command line interface
```python -m cli``` provides 2 commands for exploring SPARQL query templates discovered and associated queries of each template
* ```show-templates``` List templates sorted by number of queries associated
* ```show-queries``` Show queries belong to the given template id

For example, the following command shows the templates discovered with their template ID

```$ python -m cli show-templates```

And if we would like to see actual queries associated with template ID 1, we can use the following command with template ID = 1 provided at the end

```$ python -m cli show-queries 1```

For more details, use the ```--help``` option:

```$ python -m cli show-queries --help```
```$ python -m cli show-templates --help```
