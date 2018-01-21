from django.core.management.base import BaseCommand
from main.models import Subjects


SUBJECTS = [
    "Logic",
    "Python",
    "Html",
    "Algorithms",
    "Javascript",
    "Css",
    "Django",
    "NoSql",
    "Jquery",
    "Design patterns",
    "Sql",
    "Git",
    "Software testing",
    "Networking",
    "Machine learning",
    "Java",
    "Administration",
    "Android",
    "Security",
    "Pyramid",
    "Cpp",
]


class Command(BaseCommand):
    help = "Initialize subjects"

    def handle(self, *args, **options):
        self.stdout.write("Started subjects initialization")
        db_subjects = Subjects.objects.all()
        self._delete_subjects(db_subjects)
        self._create_subjects()
        self.stdout.write("Finished subjects initialization")

    def _delete_subjects(self, db_subjects):
        for db_subject in db_subjects:
            subject_name = db_subject.name
            if subject_name not in SUBJECTS:
                db_subject.delete()
                self.stdout.write("removed subject: '{}'".format(subject_name))

    def _create_subjects(self):
        for subject in SUBJECTS:
            subject_obj, created = Subjects.objects.get_or_create(name=subject)
            if created:
                self.stdout.write("created subject: '{}'".format(subject))
