search_body_pattern = {
    "from": 0,
    "size": 10,
    "query": {
        "bool": {
            "must": {
                "function_score": {
                    "query": {
                        "multi_match": {
                            "query": "",
                            "fields": ["name^6", "name.ngrams^2", "name.phonetic^3", "nage.autocomplete^2"],
                            "type": "best_fields"
                        }
                    },
                    "field_value_factor": {
                        "field": "search_scoring",
                        "modifier": "log1p",
                        "factor": 10
                    },
                    "boost_mode": "multiply"
                }
            },
            "filter": [
                { "term": {"is_in_stock": "true"} }
            ]
        }
    }
}


def generate_from_pattern(query):
    body = search_body_pattern.copy()
    body['query']['bool']['must']['function_score']['query']['multi_match']['query'] = query
    return body