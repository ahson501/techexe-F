# techexeapp/context_processors.py
from techexeapp.middleware import DynamicSiteIDMiddleware

def current_site_processor(request):
    # Get the current site ID using the middleware
    current_site_id = DynamicSiteIDMiddleware.get_current_site_id(request)
    return {
        'current_site_id': current_site_id
    }
