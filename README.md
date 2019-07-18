# omega-topology-MIontology

> Gives to omega-topology-graph needed ontology tree and ontology terms.

Compute a tree according to some MI ids, or give terms related to some MI ids.

> This micro-service is an REST JSON API, responding ONLY to JSON formatted requests.

## Installation

```bash
git clone https://github.com/alkihis/omega-topology-MIontology.git
mkdir ~/.envs
virtualenv --python=/usr/bin/python3.6 ~/.envs/omega-topology-MIontology
cd omega-topology-MIontology
source ~/.envs/omega-topology-MIontology/bin/activate
pip3 install flask owlready2 flask-cors
deactivate
```

## Starting the service
```bash
Usage: python src/main.py [options]

Options:
  -p, --port [portNumber]              Server port number (default: 3279)
```

- -p, --port &lt;portNumber&gt; : Port used by the micro-service to listen to request

```bash
# Enter inside the virtual env
source ./start.sh

# Run the service
python src/main.py
```

## Available endpoints

All endpoints are CORS-ready.

All endpoints use JSON-formatted body in request. In order to use JSON in body, **don't forget to add header `Content-Type: application/json`** in your request !

### POST /term
Get the term associated to a MI ID.
ID will **NOT** be automatically prefixed. Take care of putting the `MI:` behind the id.

Body must be JSON-formatted, and contain a object with one key `term`, linked to an array of stringified taxonomic ids.

- `@url` POST http://<µ-service-url>/term
- `@returns`
```json
{
    "success": true,
    "terms": {
        [mi_id: string]: string
    }
}
```

### POST /tree
Get the tree needed to link the MI ontology ids together.

Body must be JSON-formatted, and contain a object with one key `mi_ids`, linked to an array of stringified MI ontology ids.
Ids may start by `MI:` or will be automatically prefixed.

- `@url` POST http://<µ-service-url>/tree
- `@returns`
```ts
{
    "success": true,
    "tree": NodeTree
}

with interface NodeTree {
    [mi_id: string]: { children: NodeTree[], name: string }
}
```


## Examples

### Getting ontology terms according to MI ids
```bash
curl -H "Content-Type: application/json" -d '{"term":["MI:0084", "MI:0225", "MI:0841", "MI:0006"]}' http://<µ-service-url>/term
```
```json
{
    "success": true,
    "terms": {
        "MI:0006": "anti bait coimmunoprecipitation",
        "MI:0084": "phage display",
        "MI:0225": "chromatin immunoprecipitation array",
        "MI:0841": "phosphotransferase assay"
    }
}
```
---
### Getting ontology tree for the following MI ids
```bash
curl -H "Content-Type: application/json" -d '{"mi_ids":["MI:0084", "0225", "0841", "0006"]}' http://<µ-service-url>/tree
```
```json
{
    "success": true,
    "tree": {
        "MI:0001": {
            "children": {
                "MI:0045": {
                    "children": {
                        "MI:0401": {
                            "children": { 
                                "MI:0091": {
                                    "children": {
                                        "MI:0004": { 
                                            "children": {
                                                "MI:0019": {
                                                    "children": {
                                                        "MI:0006": {
                                                            "children": {},
                                                            "name": "anti bait coimmunoprecipitation"
                                                        }
                                                    },
                                                    "name": "coimmunoprecipitation"
                                                }
                                            },
                                            "name": "affinity chromatography technology"
                                        }
                                    },
                                    "name": "chromatography technology"
                                }, 
                                "MI:0400": {
                                    "children": {
                                        "MI:0008": {
                                            "children": {
                                                "MI:0225": {
                                                    "children": {},
                                                    "name": "chromatin immunoprecipitation array"
                                                }
                                            },
                                            "name": "array technology"
                                        }, 
                                        "MI:0034": {
                                            "children": {
                                                "MI:0084": {
                                                    "children": {},
                                                    "name": "phage display"
                                                }
                                            },
                                            "name": "display technology"
                                        }
                                    },
                                    "name": "affinity technology"
                                },
                                "MI:0415": {
                                    "children": {
                                        "MI:0841": {
                                            "children": {},
                                            "name": "phosphotransferase assay"
                                        }
                                    },
                                    "name": "enzymatic study"
                                }
                            },
                            "name": "biochemical"
                        }
                    },
                    "name": "experimental interaction detection"
                }
            },
            "name": "interaction detection method"
        }
    }
}
```
