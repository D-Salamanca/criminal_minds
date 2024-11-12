from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])


def elastic_create_index(index_name: str) -> None:
    index_config = {
        "mappings": {
            "properties":{
                "dbcamp":"value"
            }
        }
    }
    es.indices.create(index=index_name, body=index_config, ignore=400)


def elastic_send_data(data: str, index_name: str) -> None:
    es.index(index=index_name, body=data)

