from django.core.management.base import BaseCommand
from user_management.models import UserRole

class Command(BaseCommand):
    help = 'Populate UserRole with data'

    def handle(self, *args, **kwargs):
        roles = [
            # hms roles
            ['hms',  'HMS-WRH', 'Warehouse'],
            ['hms',  'HMS-SUR', 'Superuser/Administrator'],
            ['hms',  'HMS-KCN', 'Kitchen'],
            ['hms',  'HMS-SVR', 'Supervisor'],

            # ims roles
            ['ims',  'IMS-WRH', 'Warehouse'],
            ['ims',  'IMS-MBR', 'Member'],

            # others
            ['NUL',  'NUL-NUL', 'Unassigned'],
        ]

        for role in roles: 
            UserRole.objects.create(
                app = role[0],
                code = role[1],
                name = role[2]
            )

        self.stdout.write(self.style.SUCCESS('UserRole data populated successfully'))