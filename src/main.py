from flask import Flask, request, jsonify
import os
import json
from ontology import Ontology
from flask_cors import CORS
__dirname = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=3279, help="Port")

program_args = parser.parse_args()

app = Flask("omega-topology-MIontology")
CORS(app)

ONTOLOGY_FILE = __dirname + "/../mi.owl"
ROOT_ID = "MI:0001"

onto = Ontology(ONTOLOGY_FILE)

def constructTree(root_id, seeds):
    tree = onto.constructTreeFromRoot(root_id)
    pruned = tree.prune(seeds).toDict()

    return pruned

root_tree = onto.constructTreeFromRoot(ROOT_ID)

def getLabelOf(id):
    node = root_tree.findInTree(id)

    if node:
        return node.label
    else:
        return None

# p = open('full_tree.json', 'w')
# tree = onto.constructTreeFromRoot("MI:0001", [ 'hasExactSynonym' ])
# json.dump(tree.toDict(), p)

# testtree = constructTree("MI:0001", ["MI:2224", "MI:0398", "MI:0895", "MI:0364"])
# p = open('test.json', 'w')
# json.dump(testtree, p)

term_cache = {}

@app.route('/term', methods=['POST'])
def get_term_of():
    if not request.is_json:
        return jsonify(success=False, reason="Bad content type"), 400

    data = request.json

    if not 'term' in data:
        return jsonify(success=False, reason="Taxonomic IDs are missing"), 400

    if not isinstance(data['term'], list) and not isinstance(data['term'], str):
        return jsonify(success=False, reason="Taxonomic IDs must be sended as a string array or a simple string"), 400

    terms = {}

    if isinstance(data['term'], str):
        data['term'] = [data['term']]

    for term in data['term']:
        if term in term_cache:
            terms[term] = term_cache[term]
        else:
            term_fetched = getLabelOf(term)
            if term_fetched:
                terms[term] = term_cache[term] = term_fetched
        


    return jsonify(success=True, terms=terms)

"""
Respond a JSON containing ontology tree of requested MI IDs (MI IDs are string, under the form "MI:<integer>")
@expecting HTTP POST; Content-Type: application/json; Body: { "mi_ids" [<listofIDs>] }
@returns JSON response; Body: { success: true, tree: NodeTree }; NodeTree as { [miId: string]: { children: NodeTree[], name: string } }
"""
@app.route('/tree', methods=['POST'])
def get_taxo_of():
    if not request.is_json:
        return jsonify(success=False, reason="Bad content type"), 400

    data = request.json

    if 'mi_ids' not in data:
        return jsonify(success=False, reason="Requested IDs are missing"), 400

    if not isinstance(data['mi_ids'], list):
        return jsonify(success=False, reason="Requested IDs must be sended as a string array"), 400

    sended_list = list(map(lambda x: x if x.startswith('MI:') else 'MI:' + x, data['mi_ids']))

    # Get tree for IDs
    try:
        return jsonify(success=True, tree=constructTree(ROOT_ID, sended_list))
    except IndexError:
        return jsonify(success=False, reason="Cant create a pruned tree without any valid seed"), 404

@app.errorhandler(405) # Method Not Allowed
def method_not_allowed(e):
    return jsonify(success=False, reason="Method not allowed"), 400

@app.errorhandler(404) # Page Not Found
def page_not_found(e):
    return '', 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(success=False, reason="Unexpected internal server error", error=repr(e)), 500

# Run integrated Flask server
app.run(host='0.0.0.0', port=program_args.port)
