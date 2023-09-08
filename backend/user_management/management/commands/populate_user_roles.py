from django.core.management.base import BaseCommand
from user_management.models import UserRole

class Command(BaseCommand):
    help = 'Populate UserRole with data'

    def handle(self, *args, **kwargs):
        # hms roles
        hms_roles = [
            ['hms',  'HMS-WRH', 'Warehouse'],
            ['hms',  'HMS-SUR', 'Superuser/Administrator Role'],
            ['hms',  'HMS-KCN', 'Kitchen'],
            ['hms',  'HMS-SVR', 'Supervisor'],
            ['hms',  'HMS-UAN', 'Unassigned'],
        ]

        for hms_role in hms_roles: 
            UserRole.objects.create(
                app = hms_role[0],
                code = hms_role[1],
                name = hms_role[2]
            )

        self.stdout.write(self.style.SUCCESS('UserRole data populated successfully'))