import utils
from django.conf import settings

def consent_provider(request):
    """
    Add Mamoto consent script to the requests context.
    :Cases:
        - If MATOMO_REQURE_CONSENT is True OR If ALWAYS_TRACK_REGISTERED True == continue on
        - If ALWAYS_TRACK_REGISTERED is True AND the user is authenticated
    """
    # Do we require consent?
    if getattr(settings, 'MATOMO_REQUIRE_CONSENT', False):
        provide_script = True
        if request.user.is_authenticated and not getattr(settings, "ALWAYS_TRACK_REGISTERED", True):
            provide_script = False
        if provide_script:
            grant_class_name = getattr(settings, 'GRANT_CONSENT_TAG_CLASSNAME')
            revoke_class_name = getattr(settings, 'REVOKE_CONSENT_CLASSNAME')
            return {"consent_script":"""
            %s;
            %s
            %s
            """ % (
                utils.build_paq_cmd('requireConsent'),
                utils.get_event_bind_js(
                    class_name=grant_class_name,
                    matomo_event="rememberConsentGiven",
                ),
                utils.get_event_bind_js(
                    class_name=revoke_class_name,
                    matomo_event="forgetConsentGiven",
                )
            )}
    return {'consent_script': ""}
