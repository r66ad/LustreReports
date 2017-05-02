from django.core.management import BaseCommand
 #The class must be named Command, and subclass BaseCommand

class Command(BaseCommand):
    help = "Generates pdf from svg charts in tmp directory."
