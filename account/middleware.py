from .models import IPAddress


# A custom middleware which gets the user ip address and store it as a new attribute for user object
class IPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        content = request.META.get('HTTP_X_FORWARDED_FOR')
        if content:
            ip_address = content.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        ip, created = IPAddress.objects.get_or_create(ip_address=ip_address)

        request.user.ip_address = ip

        # Everything which should be done before the response get ready should be written above this line
        response = self.get_response(request)
        # And every thing which should be written when response got ready or view called should be bellow

        return response
