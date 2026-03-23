def check_data(name, login, password):
    if (name is None) or (len(login) < 4) or (len(password) < 8):
        return True 
    else:
        return False