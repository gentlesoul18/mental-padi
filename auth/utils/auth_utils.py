from bcrypt import hashpw, gensalt, checkpw


def get_hashed_password(plain_password: str) -> str:
    """
    Hashes a plain password using bcrypt.
    
    Args:
        plain_password (str): The plain password to hash.
        
    Returns:
        str: The hashed password.
    """
    return hashpw(plain_password.encode('utf-8'), gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password using bcrypt.
    
    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to check against.
        
    Returns:
        bool: True if the passwords match, False otherwise.
    """

    try: 
        return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        print(f"Error verifying password: {ValueError}")
        return False