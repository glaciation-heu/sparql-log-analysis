import typer
import pickle

from rich import print
from rich.console import Console
from rich.table import Table


console = Console()

app = typer.Typer(
    help='''
        Welcome to GLACIATION SPARQL query explorer, which contains queries grouped by templates. 

        In template, the same pattern but with different literals or IRIs represented by variables with $_x format. 

        For example, both queries below:

        ------------------------------------------

        SELECT ?director ?starring WHERE {
        
        dbr:Pulp_Fiction dbo:director ?director .
        
        dbr:Pulp_Fiction dbo:starring ?starring .
        
        }

        ------------------------------------------

        SELECT ?director ?starring WHERE {

        dbr:Django_Unchained dbo:director ?director .

        dbr:Django_Unchained dbo:starring ?starring .

        }

        ------------------------------------------

        will belong to the following SPARQL template

        ------------------------------------------

        SELECT ?director ?starring WHERE {

        $_1 dbo:director ?director .

        $_1 dbo:starring ?starring .

        }

        ------------------------------------------
        
        GLACIATION upper ontology can be found at: https://glaciation-project.eu/MetadataReferenceModel/1.1.0/
        ''',
    no_args_is_help=True
)


def load_templates(
    file: str = 'db/templates.pkl',
):
    with open(file, 'rb') as f:
        template_dict = pickle.load(f)

    # Sorting
    template_dict = dict(
        sorted(
            template_dict.items(), 
            key=lambda x: len(x[1][0]), 
            reverse=True
        )
    )

    return template_dict


@app.command()
def show_templates(
    n: int = 5
):
    '''
    List templates sorted by number of queries

    Args:
        n: top-n templates to return
    '''
    template_dict = load_templates()
    print(f'{len(template_dict.keys())} existing templates')

    table = Table('Template ID', 'Template', '# of Queries')
    for ind, val in enumerate(list(template_dict.keys())[:n]):
        table.add_row(str(ind), val, str(len(template_dict[val][0])))

    console.print(table)


@app.command()
def show_queries(
    template_id: int,
    n: int = 1
):
    '''
    Show queries belonging to the given template_id

    Args:
        template_id: to search queries
        n: first-n queries
    '''
    template_dict = load_templates()

    if template_id in list(range(len(template_dict.keys()))):
        template = list(template_dict.keys())[template_id]

    #print(template)
    table = Table('Query Index', 'Query')
    for ind, mapping in enumerate(template_dict[template][0][:n]):
        # Use mapping to construct back original queries
        query = template
        for key in list(mapping.keys())[::-1]:
            query = query.replace(key, mapping[key])
        table.add_row(str(ind), str(query))
        
    console.print(table)


if __name__ == '__main__':
    app()
