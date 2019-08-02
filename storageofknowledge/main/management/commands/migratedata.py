import json
from django.core.management.base import BaseCommand
from main.models import *


"""
1. add old models to models.py
2. add `old_db` to settings DATABASES
"""

SUBJECT_MAP = {
    # old: new
}


USER_MAP = {
    # old: new
}


OLD_ITEM_OLD_USER_MAP = {
    # old item id: old user id
}


OLD_ITEM_OLD_TYPE_NAME_MAP = {
    # old item id: old type name
}


class Command(BaseCommand):
    help = "Migrate data to a new schema"

    def handle(self, *args, **options):
        self.stdout.write("Started data migration")
        # self.save_old_user_relations()
        # self.save_old_type_relations()

        self.process_users()
        self.process_subjects()
        self.process_notes()
        self.process_links()
        self.process_likes_dislikes()
        self.process_comments()

        self.stdout.write("Finished data migration")

    def save_old_user_relations(self):
        old_items = Comments.objects.using('old_db').all()

        for item in old_items:
            OLD_ITEM_OLD_USER_MAP[item.id] = item.user.id

        with open('old_relations/comments.json', 'w') as f:
            json.dump(OLD_ITEM_OLD_USER_MAP, f)

    def save_old_type_relations(self):
        old_items = LikesDislikes.objects.using('old_db').all()

        for item in old_items:
            OLD_ITEM_OLD_TYPE_NAME_MAP[item.id] = item.type.type_name

        with open('old_relations/like_dislike_types.json', 'w') as f:
            json.dump(OLD_ITEM_OLD_TYPE_NAME_MAP, f)

    def process_notes(self):
        self.stdout.write("started processing notes")

        old_notes = Notes.objects.using('old_db').all()
        with open('old_relations/notes.json') as f:
            old_note__old_user_id = json.load(f)

        for old_note in old_notes:
            old_user_id = old_note__old_user_id[str(old_note.id)]
            user = User.objects.using('default').get(id=USER_MAP[old_user_id])

            subject = Subject.objects.using('default').get(id=SUBJECT_MAP[old_note.subject.id])

            new_note, _ = Note.objects.get_or_create(
                topic=old_note.topic,
                user=user,
            )

            new_note.body = old_note.body
            new_note.private = old_note.private
            new_note.subjects.add(subject)
            new_note.save(using='default')

        self.stdout.write("finished processing notes")

    def process_links(self):
        self.stdout.write("started processing links")

        old_links = Links.objects.using('old_db').all()
        with open('old_relations/links.json') as f:
            old_link__old_user_id = json.load(f)

        for old_link in old_links:
            old_user_id = old_link__old_user_id[str(old_link.id)]
            user = User.objects.using('default').get(id=USER_MAP[old_user_id])

            subject = Subject.objects.using('default').get(id=SUBJECT_MAP[old_link.subject.id])

            new_link, _ = Link.objects.get_or_create(
                name=old_link.link_name,
                user=user,
            )

            new_link.link = old_link.link
            new_link.private = False
            new_link.subjects.add(subject)
            new_link.save(using='default')

        self.stdout.write("finished processing links")

    def process_likes_dislikes(self):
        self.stdout.write("started processing likes and dislikes")

        old_likes_dislikes = LikesDislikes.objects.using('old_db').all()
        with open('old_relations/like_dislike.json') as f:
            old_ld__old_user_id = json.load(f)

        with open('old_relations/like_dislike_types.json') as f:
            old_ld__old_type_name = json.load(f)

        for old_ld in old_likes_dislikes:
            old_user_id = old_ld__old_user_id[str(old_ld.id)]
            old_type_name = old_ld__old_type_name[str(old_ld.id)]

            user = User.objects.using('default').get(id=USER_MAP[old_user_id])

            if old_type_name.endswith('links'):
                old_link = Links.objects.using('old_db').get(id=old_ld.resource_id)
                new_link = Link.objects.get(name=old_link.link_name)

                if old_ld.like:
                    LinkLike.objects.create(link=new_link, user=user)
                elif old_ld.dislike:
                    LinkDislike.objects.create(link=new_link, user=user)

            elif old_type_name.endswith('notes'):
                old_note = Notes.objects.using('old_db').get(id=old_ld.resource_id)
                new_note = Note.objects.get(topic=old_note.topic)

                if old_ld.like:
                    NoteLike.objects.create(note=new_note, user=user)
                elif old_ld.dislike:
                    NoteDislike.objects.create(note=new_note, user=user)

            else:
                raise ValueError('unknown type name: {}'.format(old_type_name))

        self.stdout.write("finished processing likes and dislikes")

    def process_comments(self):
        self.stdout.write("started processing comments")

        old_comments = Comments.objects.using('old_db').all()
        with open('old_relations/comments.json') as f:
            old_comment__old_user_id = json.load(f)

        for old_comment in old_comments:
            old_user_id = old_comment__old_user_id[str(old_comment.id)]

            user = User.objects.using('default').get(id=USER_MAP[old_user_id])

            old_note = Notes.objects.using('old_db').get(id=old_comment.resource_id)
            new_note = Note.objects.get(topic=old_note.topic)

            new_note.comments.create(
                user=user,
                comment=old_comment.comment
            )

        self.stdout.write("finished processing comments")

    def process_subjects(self):
        self.stdout.write("started processing subjects")
        old_subjects = Subjects.objects.using('old_db').all()

        for old_sub in old_subjects:
            new_sub, _ = Subject.objects.get_or_create(
                name=old_sub.name
            )
            SUBJECT_MAP[old_sub.id] = new_sub.id.hex
        self.stdout.write("finished processing subjects")

    def process_users(self):
        self.stdout.write("started processing users")
        old_users = {
            'artem': {
                'id': 1,
                'password': 'pbkdf2_sha256$36000$chmhvL4UCtfR$IuvDsdv2TO6QR9qRtZ4aBgtOmSVqBht9EZcVflOZB+k=',
                'is_superuser': True,
                'is_staff': True,
                'email': 'ArtyomSliusar@gmail.com',
            },
            'kpishnik': {
                'id': 3,
                'password': 'pbkdf2_sha256$20000$RApKvsONbnnu$xW6nnuZK3FTFz+NHpy/iL+dAWbgvLmtlC8kIDwIOjtg=',
                'is_superuser': False,
                'is_staff': False,
                'email': 'zelinskij@bkc.com.ua',
            },
            'Skident': {
                'id': 4,
                'password': 'pbkdf2_sha256$20000$24tvNoBOaFiI$putcypApwvsgmywWD+tUKSWHclFXe/+o/UBM4x2prFM=',
                'is_superuser': False,
                'is_staff': False,
                'email': 'bagriy.volodymyr@gmail.com',
            }
        }

        for old_username, old_user_data in old_users.items():
            new_user, created = User.objects.get_or_create(
                username=old_username
            )

            if created:
                new_user.email = old_user_data['email']
                new_user.is_superuser = old_user_data['is_superuser']
                new_user.is_staff = old_user_data['is_staff']
                new_user.password = old_user_data['password']
                new_user.is_active = True
                new_user.time_zone = 'Europe/Kiev'
                new_user.save(using='default')
            USER_MAP[old_user_data['id']] = new_user.id

        self.stdout.write("finished processing users")
