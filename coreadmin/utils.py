def is_core_admin(user):
    if user.is_authenticated:
        return user.is_core_admin
    else:
        return False
    
def not_core_admin(user):
    if user.is_authenticated:
        return not user.is_core_admin
    else:
        return True