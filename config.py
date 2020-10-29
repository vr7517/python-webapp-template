class BaseConfig(object):
    # Can be set to 'MasterUser' or 'ServicePrincipal'
    AUTHENTICATION_MODE = 'MasterUser'

    # Workspace Id in which the report is present
    WORKSPACE_ID = 'ff97de67-0527-4671-acea-28c8c679e79c'
    
    # Report Id for which Embed token needs to be generated
    REPORT_ID = '3e3030f3-f0a5-4489-9c59-d9661fb52302'
    
    # Id of the Azure tenant in which AAD app and Power BI report is hosted. Required only for ServicePrincipal authentication mode.
    TENANT_ID = '51c8caaa-6de7-45ac-9f92-cb78cf215347'
    
    # Client Id (Application Id) of the AAD app
    CLIENT_ID = 'cd03c373-7b16-492a-a7b4-8e5a122b96ad'
    
    # Client Secret (App Secret) of the AAD app. Required only for ServicePrincipal authentication mode.
    CLIENT_SECRET = ''
    
    # Scope of AAD app. Use the below configuration to use all the permissions provided in the AAD app through Azure portal.
    SCOPE = ['https://analysis.windows.net/powerbi/api/.default']
    
    # URL used for initiating authorization request
    AUTHORITY = 'https://login.microsoftonline.com/organizations'
    
    # Master user email address. Required only for MasterUser authentication mode.
    POWER_BI_USER = 'hari@irislogic.com'
    
    # Master user email password. Required only for MasterUser authentication mode.
    POWER_BI_PASS = 'Om$1990dec'