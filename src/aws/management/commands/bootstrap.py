from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('migrate')
        call_command('collectstatic', '--noinput')
