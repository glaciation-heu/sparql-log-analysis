from rdflib.plugins.sparql import parser
from rdflib.plugins.sparql import algebra
from collections import defaultdict

import re
import os
import glob
import data_utils
import logging
import pandas as pd
import subprocess
logger = logging.getLogger(__name__)


LOG_FOLDER = 'log_analysis/logs/'


def load_queries(filename: str) -> list:
    """ Load list of queries from file """
    queries = list()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            queries = f.readlines()

    return queries


def normalize(query_file: str, num: int) -> list:
    """ Return normalized queries using Qcan libray """
    # clean up the folder
    subprocess.run('rm resultFiles/*', shell=True, check=True)

    # execute Qcan
    for i in range(num):
        subprocess.run(['java', 
            '-jar', 
            'QCan/target/qcan-1.1-jar-with-dependencies.jar',
            'benchmark',
            '-x',
            query_file,
            '-n',
            str(i+1),
            '-o',
            str(i),
            '-d'
        ])
        break
    
    # process the output file
    pattern = 'resultFiles/*_dist*.log'
    log_file = glob.glob(pattern)[0]
    logger.debug(f'log file: {log_file}')

    with open(log_file, 'r') as f:
        lines = f.readlines()
        print(lines)





def is_keyword(term: str) -> bool:
    """ Check if it is a SPARQL keyword """
    if term.lower() in [x.lower() for x in data_utils.KEYWORDS]:
        return True
    return False

def is_symbol(term: str) -> bool:
    """ Check if it is a symbol """
    if term in data_utils.SYMBOLS:
        return True
    return False

def is_var(term: str) -> bool:
    """ Check if it is a variable """
    if term.startswith('?'):
        return True
    return False

def replace_values(query: str) -> str:
    """ Concatenate values in VALUES clause """
    pattern = r'VALUES[^{]*(\{[^}]*\})'
    matches = re.findall(pattern, query)
    for values in matches:
        logger.debug(f'Values: {values}')
        query = query.replace(
            values, 
            values.replace(' ', '')
        )

    logger.debug(f'Updated query after relacing values: {query}')
    return query



def generalize(query: str) -> tuple:
    """ Generalize the query
        Return (template, mapping)
    """
    mapping = dict()
    query = query.strip()

    # Expand () with front and rear spaces
    for i in ['(', ')']:
        query = query.replace(i, ' '+i+' ')

    # Special care of VALUES
    query = replace_values(query)
    
    terms = query.strip().split()
    rdf_term_idx = 1
    # To order vars
    var_dict = dict()
    for i, t in enumerate(terms):
        t = t.strip()
        if (t != '' and 
            not is_keyword(t) and  
            not is_symbol(t) and  
            not is_var(t)): 
            # Log terms
            logger.debug(f'Deteted term:{t}, {len(t)}')
            terms[i] = f'$_{rdf_term_idx}'
            mapping[f'$_{rdf_term_idx}'] = t
            rdf_term_idx += 1
        # Update vars and names to be changed with order
        if t.startswith('?') and t not in var_dict:
            var_dict[t] = f'?var{len(var_dict)}'
    template = ' '.join(terms)

    # Update var names to be in order
    for var in var_dict:
        template = template.replace(var, var_dict[var])

    logger.info(f'Updated tempalte after Generalization step: {template}')
    logger.debug(f'mapping: {mapping}')
    print('')
    
    return template, mapping


def specialize(template: str, mapping: list) -> dict:
    """ Update the template 
    """
    # If mappings of a parameter are all the same
    # specify that instead of parameter
    params = list()
    for param in mapping[0]:
        param_val = mapping[0][param]
        all_mapping_the_same = True
        if len(mapping) == 1:
            all_mapping_the_same = False
        else:
            for m in mapping:
                if m[param] != param_val:
                    all_mapping_the_same = False
        if all_mapping_the_same:
            params.append(param)
            
    for param in params:
        template = template.replace(param, param_val)
        for m in mapping:
            m.pop(param)

    return template, mapping


def discover_templates(queries: list):
    """ Discover all templates regarding input queries """

    df = pd.DataFrame({'Q': queries, 'T_specialized': None, 'T_generalized': None})
    # Store mappings of each query to the template
    template_mappings = defaultdict(list)
    # Store corresponding query index
    template_queries = defaultdict(list)
    templates = list()
    for i, q in enumerate(queries):
        logger.debug('#'*25+f'Query {i}'+'#'*25)
        logger.debug(q)
        template, mapping = generalize(q)
        template_mappings[template].append(mapping)
        template_queries[template].append(i)
        templates.append(template)
    df['T_generalized'] = templates

    logger.debug(f'Mappings: {dict(zip(template_mappings.keys(), [len(x) for x in template_mappings.values()]))}')

    template_mappings_specialized = defaultdict(list)
    for t in template_mappings:
        template_specialized, mapping_specialized = specialize(t, template_mappings[t])
        template_mappings_specialized[template_specialized].append(mapping_specialized)
        df[df['T_generalized'] == t] = template_specialized

    logger.debug(f'Mappings specialized: {template_mappings_specialized}')

    # Store to disk
    for col in ['T_generalized', 'T_specialized']:
        with open(f'{LOG_FOLDER}{col}','w') as f:
            for val in df[col]:
                f.write(val+'\n')

    return template_queries, template_mappings_specialized


def main():
    """ """
    logging.basicConfig(
        #filename='main.log', 
        level=logging.DEBUG
    )

    queries = load_queries(f'{LOG_FOLDER}distinct_sorted_queries.txt')
    logger.info(f'{len(queries)} are loaded')

    queries_normalized = normalize(
        f'{LOG_FOLDER}distinct_sorted_queries.txt',
        len(queries)
    )

    #discover_templates(queries)


if __name__ == '__main__':
    main()
