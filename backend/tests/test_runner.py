from django.test.runner import DiscoverRunner
from django.conf import settings

class RemoteHerokuTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return {
            'default': {
                'NAME': settings.DATABASES['test']['NAME'],
            },
        }
    
    # no need to teardown remote db
    def teardown_databases(self, old_config, **kwargs):
        pass