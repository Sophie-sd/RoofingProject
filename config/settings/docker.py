from urllib.parse import urlparse

from decouple import config

from .production import *  # noqa: F403

# TLS terminates in nginx; Gunicorn serves HTTP only.
# SECURE_SSL_REDIRECT=True would break container healthchecks (301).
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB', default='roofing'),
        'USER': config('POSTGRES_USER', default='roofing'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DB_HOST', default='db'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

_site_url = config('SITE_URL', default='').strip().rstrip('/')
if _site_url:
    _hostname = urlparse(_site_url).hostname
    if _hostname:
        _host_candidates = {_hostname}
        if _hostname.startswith('www.'):
            _host_candidates.add(_hostname[4:])
        else:
            _host_candidates.add(f'www.{_hostname}')
        for _host in _host_candidates:
            if _host and _host not in ALLOWED_HOSTS:  # noqa: F405
                ALLOWED_HOSTS.append(_host)  # noqa: F405
    if _site_url not in CSRF_TRUSTED_ORIGINS:  # noqa: F405
        CSRF_TRUSTED_ORIGINS.append(_site_url)  # noqa: F405

for _internal_host in ('127.0.0.1', 'localhost', 'web'):
    if _internal_host not in ALLOWED_HOSTS:  # noqa: F405
        ALLOWED_HOSTS.append(_internal_host)  # noqa: F405
