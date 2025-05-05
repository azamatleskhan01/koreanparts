from django.core.management.base import BaseCommand
from django.apps import apps
import graphviz

class Command(BaseCommand):
    help = 'Generate GraphViz diagram of models'

    def handle(self, *args, **options):
        dot = graphviz.Digraph(comment='Django Models')
        for model in apps.get_models():
            fields = [f"{f.name}: {f.__class__.__name__}" for f in model._meta.get_fields()]
            dot.node(model.__name__, label="{\n" + "\n".join(fields) + "}")
            for f in model._meta.get_fields():
                if f.is_relation and f.related_model:
                    dot.edge(model.__name__, f.related_model.__name__, label=f.name)
        dot.render('models.gv', view=False)
