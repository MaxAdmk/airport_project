from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class AuthenticationThrottle(UserRateThrottle):
    scope = 'authentication'
    
class StandardUserThrottle(UserRateThrottle):
    scope = 'user'
    
class AnonymousUserThrottle(AnonRateThrottle):
    scope = 'anon'