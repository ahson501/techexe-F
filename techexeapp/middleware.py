# techexeapp/middleware.py
from django.conf import settings
from django.contrib.sites.models import Site

class DynamicSiteIDMiddleware:
    """
    Middleware to dynamically set the SITE_ID based on the request's domain.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine the domain from the request
        domain = request.get_host().split(':')[0]  # Remove port number if present
        
        # Find the Site object based on the domain
        try:
            site = Site.objects.get(domain=domain)
            settings.SITE_ID = site.id  # Set the SITE_ID dynamically
        except Site.DoesNotExist:
            # If the site is not found, set to a default SITE_ID (you can change this as needed)
            settings.SITE_ID = 1  # Default to the first site

        # Call the next middleware
        response = self.get_response(request)
        return response

    @staticmethod
    def get_current_site_id(request):
        """
        Returns the current site ID based on the request domain.
        """
        domain = request.get_host().split(':')[0]  # Remove port number if present
        try:
            site = Site.objects.get(domain=domain)
            return site.id
        except Site.DoesNotExist:
            return 1  # Default site ID
