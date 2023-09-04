def has_access_level(user, access_levels: list):
    return user.profile.access_level in access_levels

def has_role(user, role_codes: list):
    for user_role in user.profile.user_roles.all():
        for role_code in role_codes:
            if role_code in user_role.code:
                return True
    return False 