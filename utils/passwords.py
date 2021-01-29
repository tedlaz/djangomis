import hashlib, binascii, os

ROUNDS = 120345
SIZE = 15


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')[:10]
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                salt, ROUNDS, SIZE)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:10]
    stored_password = stored_password[10:]
    pwdhash = hashlib.pbkdf2_hmac('sha256', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  ROUNDS, SIZE)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
