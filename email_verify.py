import re

def is_valid_email(email):
    """
    Validate an email address.

    Parameters:
    - email (str): The email address to validate.

    Returns:
    - bool: True if the email is valid, False otherwise.
    """
    # Define the regular expression pattern for a simple email validation
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'

    # Use re.match to check if the email matches the pattern
    match = re.match(pattern, email)

    # Return True if there is a match, indicating a valid email address
    return match is not None