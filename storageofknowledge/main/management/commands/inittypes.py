from django.core.management.base import BaseCommand
from main.models import TypeTable


TYPES = [
    "learn_links",
    "check_links",
    "note_notes",
]


class Command(BaseCommand):
    help = "Initialize types"

    def handle(self, *args, **options):
        self.stdout.write("Started types initialization")
        db_types = TypeTable.objects.all()
        self._delete_types(db_types)
        self._create_types()
        self.stdout.write("Finished types initialization")

    def _delete_types(self, db_types):
        for db_type in db_types:
            type_name = db_type.type_name
            if type_name not in TYPES:
                db_type.delete()
                self.stdout.write("removed type: '{}'".format(type_name))

    def _create_types(self):
        for _type in TYPES:
            subject_obj, created = TypeTable.objects.get_or_create(type_name=_type)
            if created:
                self.stdout.write("created type: '{}'".format(_type))
