from django.core.management.base import BaseCommand
from django.db import connection, transaction

from render.models import Students


class Command(BaseCommand):
    help = 'Renumber student ids so they run 1, 2, 3 ... with no gaps.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would change without writing to the database.',
        )

    def handle(self, *args, **options):
        # Ordered by student_id so the renumbered ids line up with the business
        # ids (101 -> 1, 102 -> 2 and so on) instead of following creation order.
        students = list(Students.objects.order_by('student_id', 'id'))

        if not students:
            self.stdout.write('No students found, nothing to do.')
            return

        self.stdout.write(f'Renumbering {len(students)} student ids from 1...')

        if options['dry_run']:
            for index, student in enumerate(students, start=1):
                self.stdout.write(f'  id {student.pk} -> {index}  ({student.student_name})')
            self.stdout.write(self.style.WARNING('Dry run only, nothing was saved.'))
            return

        # The whole thing runs as one transaction, so a failure halfway leaves
        # the table exactly as it was rather than half renumbered.
        with transaction.atomic():
            # Step 1: push every id far out of the way first. Assigning 1, 2, 3
            # directly would collide with rows that already hold those ids, so
            # the whole table is parked in a range nothing is using.
            #
            # Note: update() needs the real field name 'id'. The 'pk' alias
            # only works for reading, not for writing.
            for student in students:
                Students.objects.filter(id=student.id).update(id=student.id + 1000000)

            # Step 2: now nothing is in the way, so the clean ids can be handed
            # out in order.
            for new_id, student in enumerate(students, start=1):
                Students.objects.filter(id=student.id + 1000000).update(id=new_id)

            # Step 3: clear the autoincrement counter. SQLite keeps a hidden
            # table recording the highest id it has ever handed out, and it
            # never counts backwards even after deletes. Wiping that row makes
            # the next insert pick up from max(id) + 1 again, which is why
            # numbering restarted at 8 in the first place.
            if connection.vendor == 'sqlite':
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM sqlite_sequence WHERE name = 'render_students'"
                    )

        self.stdout.write(self.style.SUCCESS('Done. Student ids now start from 1.'))
