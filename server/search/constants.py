INDEX_SETTINGS = {
    "settings": {
        "analysis": {
            "analyzer": {
                "autocomplete_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "autocomplete_filter"]
                },
                "phonetic_analyzer": {
                    "type": "custom",
                    "filter": [
                        "lowercase",
                        "russian_morphology",
                        "phonetic_cyrillic",
                        "phonetic_english"
                    ],
                    "tokenizer": "standard"
                },
                "ngram_analyzer": {
                    "type": "custom",
                    "filter": "lowercase",
                    "tokenizer": "ngram_tokenizer"
                }
            },
            "filter": {
                "phonetic_cyrillic": {
                    "type": "phonetic",
                    "encoder": "beider_morse",
                    "rule_type": "approx",
                    "name_type": "generic",
                    "languageset": ["cyrillic"]
                },
                "phonetic_english": {
                    "type": "phonetic",
                    "encoder": "beider_morse",
                    "rule_type": "approx",
                    "name_type": "generic",
                    "languageset": ["english"]
                },
                "autocomplete_filter": {
                    "type":     "edge_ngram",
                    "min_gram": 1,
                    "max_gram": 20
                }
            },
            "tokenizer": {
                "ngram_tokenizer": {
                    "type": "ngram",
                    "min_gram": 3,
                    "max_gram": 10,
                    "token_chars": [
                        "letter",
                        "digit"
                        ]
                }
            }
        }
    }
}

MAPPING_SETTINGS = {
    "product": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "standard",
                "fields": {
                    "ngrams": {
                        "type": "text",
                        "analyzer": "ngram_analyzer"
                    },
                    "phonetic": {
                        "type": "text",
                        "analyzer": "phonetic_analyzer"
                    },
                    "autocomplete": {
                        "type": "text",
                        "analyzer": "autocomplete_analyzer",
                        "search_analyzer": "standard"
                    }
                }
            },
            "search_scoring": {
                "type": "integer"
            },
            "vendor_code": {
                "type": "keyword",
                "index": "not_analyzed"
            },
            "vendor": {
                "type": "keyword",
                "index": "not_analyzed"
            },
            "is_in_stock": {
                "type": "boolean"
            }
        }
    }
}
