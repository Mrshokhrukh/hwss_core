from datetime import date

def calculate_age(born):
    """
    Calculate the age based on the provided date of birth.
    
    Args:
    - born (date): The date of birth.
    
    Returns:
    - int: The age calculated in years.
    """
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age
