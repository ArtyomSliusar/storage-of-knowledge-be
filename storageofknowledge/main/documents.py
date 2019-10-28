from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Q
from .models import Note, Link


@registry.register_document
class NoteDocument(Document):
    subjects = fields.TextField(attr="subjects_to_string")
    user = fields.ObjectField(properties={'username': fields.TextField()})
    title_suggestions = fields.CompletionField(attr='title')

    class Index:
        name = 'notes'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Note

        fields = [
            'title',
            'body',
            'private'
        ]

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
        name = 'links'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Link

        fields = [
            'title',
            'link',
            'private'
        ]

    @staticmethod
    def build_query(search_query):
        return Q("match", title={'query': search_query, 'boost': 5}) \
                | Q("match", subjects={'query': search_query, 'boost': 5}) \
                | Q("match_phrase_prefix", title={'query': search_query, 'max_expansions': 10}) \
                | Q("match", title={'query': search_query, 'fuzziness': 'AUTO'}) \
                | Q("match", link={'query': search_query, 'fuzziness': 'AUTO'}) \
                | Q("match_phrase_prefix", link={'query': search_query, 'max_expansions': 3})
