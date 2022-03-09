from datetime import datetime

def actual_datetime_string():
    return  datetime.now().strftime("%Y%m%d_%H%M%S")

def alpha_numeric_string_16():
    return ''.join(random.choice('0123456789qwertyuioplkjhgfdsazxcvbnm') for i in range(16))
