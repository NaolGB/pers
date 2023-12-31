from user_management.models import UserAccessLevel
def has_access_level(user, access_levels: list):
    return user.profile.access_level in access_levels

def has_role(user, role_codes: list):
    for user_role in user.profile.user_roles.all():
        for role_code in role_codes:
            if role_code in user_role.code:
                return True
    return False 

def get_redirect(user):
    if has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER]):
        return 'power_user_dashboard'
    if has_access_level(user, [UserAccessLevel.FUNCTIONAL_LEADER]):
        if has_role(user, ['HMS-WRH']):
            return 'warehouse_dashboard'
    if has_access_level(user, [UserAccessLevel.FUNCTIONAL_USER]):
        if has_role(user, ['HMS-KCN']):
            return 'kitchen_dashboard'
    return 'landing_home'