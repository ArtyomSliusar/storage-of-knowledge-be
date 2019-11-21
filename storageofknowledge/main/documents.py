from enum import unique, Enum
from typing import Union
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Q
from .models import Note, Link


@unique
class Indices(Enum):
    NOTES = 'notes'
    LINKS = 'links'


def get_title_suggestions(document_model: Union["NoteDocument", "LinkDocument"], query: str) -> list:
    es_suggestions = document_model.search().suggest(
        'suggestions',
        query,
        completion={'field': 'title_suggestions'}
    ).execute()

    # can't properly filter suggestions using context suggester, because of the issue:
    # https://github.com/elastic/elasticsearch/issues/30884
    # that is why have to filter suggestions after retrieving them from ES
    public_suggestions = [o for o in es_suggestions.suggest.suggestions[0].options if o['_source'].private is False]
    return public_suggestions


@registry.register_document
class NoteDocument(Document):
    subjects = fields.TextField(attr="subjects_to_string")
    user = fields.ObjectField(properties={'username': fields.TextField()})
    title_suggestions = fields.CompletionField(attr='title')

    class Index:
        name = Indices.NOTES.value
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Note

        fields = [
            'title',
            'body',
            'private'
        ]

    @classmethod
    def get_suggestions(cls, query):
        return get_title_suggestions(cls, query)

    @staticmethod
    def build_query(search_query):
        return Q("match", title={'query': search_query, 'boost': 5}) \
                | Q("match", subjects={'query': search_query, 'boost': 4}) \
                | Q("match_phrase_prefix", title={'query': search_query, 'max_expansions': 10}) \
                | Q("match", title={'query': search_query, 'fuzziness': 'AUTO'}) \
                | Q("match", body={'query': search_query, 'fuzziness': 'AUTO'}) \
                | Q("match_phrase_prefix", body={'query': search_query, 'max_expansions': 3})


@registry.register_document
class LinkDocument(Document):
    subjects = fields.TextField(attr="subjects_to_string")
    user = fields.ObjectField(properties={'username': fields.TextField()})
    title_suggestions = fields.CompletionField(attr='title')

    class Index:
        name = Indices.LINKS.value
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Link

        fields = [
            'title',
            'link',
            'private'
        ]

    @classmethod
    def get_suggestions(cls, query):
        return get_title_suggestions(cls, query)

    @staticmethod
    def build_query(search_query):
        return Q("match", title={'query': search_query, 'boost': 5}) \
                | Q("match", subjects={'query': search_query, 'boost': 5}) \
                | Q("match_phrase_prefix", title={'query': search_query, 'max_expansions': 10}) \
                | Q("match", title={'query': search_query, 'fuzziness': 'AUTO'}) \
                | Q("match", link={'query': search_query, 'fuzziness': 'AUTO'}) \
                | Q("match_phrase_prefix", link={'query': search_query, 'max_expansions': 3})


INDEX_DOCUMENT_MAP = {
    Indices.NOTES.value: NoteDocument,
    Indices.LINKS.value: LinkDocument
}
