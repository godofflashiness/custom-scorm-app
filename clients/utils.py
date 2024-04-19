def is_client_admin(user):
    if user.is_authenticated:
        return user.is_client_admin
    else:
        return False
    
def not_client_admin(user):
    if user.is_authenticated:
        return not user.is_client_admin
    else:
        return True