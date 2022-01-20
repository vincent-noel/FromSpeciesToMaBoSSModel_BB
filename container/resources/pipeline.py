import sys
import pandas as pd
import matplotlib.pyplot as plt
#importing legacy, which is the 'old' version of pypath, the only one (for now), with the graph object implemented
from pypath.legacy import main as legacy

import pypath_functions as pf
import maboss
import pandas as pd


def main(list_genes_file, bnd_file, cfg_file):
    pw_legacy = legacy.PyPath()

    # source = ["signor"]
    pickle_file = "/opt/network.pickle"
    graph = pf.load_network_from_pickle(pw_legacy, pickle_file)

    # Import a list of genes from a file
    genes = pd.read_csv(list_genes_file)
    gene_list = []
    for gene in genes.values:
        gene_list.append(str(gene[0]))


    # gene_dict = pf.generate_dict(gene_list, pw_legacy)

    # We start by associating the uniprot IDs from a gene list

    sources = gene_list
    uniprot_dict = pf.generate_dict(sources,pw_legacy)
    # The subgraph is built

    subg1 = graph.induced_subgraph([pw_legacy.vs.find(name = uniprot_dict[e]) for e in uniprot_dict.keys()])

    # According to the depth f search (distance between two nodes), we can search in the databases all the possible paths of length==depth 
    # and add all the nodes found in the graph (this can take some time depending on the depth)

    connected_dict = pf.complete_connection(subg1, uniprot_dict, 2, pw_legacy)
    subg2 = graph.induced_subgraph([pw_legacy.vs.find(name = connected_dict[e]) for e in connected_dict.keys()])


    pf.write_bnet(subg2, connected_dict, name="/tmp/model.bnet")

    model = maboss.loadBNet("/tmp/model.bnet")
    with (open(bnd_file, "w") as bnd_file, open(cfg_file, "w") as cfg_file):
        model.print_bnd(bnd_file)
        model.print_cfg(cfg_file)
        
    
    
if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))  # next section explains the use of sys.exit