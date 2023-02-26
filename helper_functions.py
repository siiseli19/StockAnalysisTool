def check_negative_cf(str):
    for i in str:
        if i == '(':
            return True
        else: return False


def check_millions_cf(str):
    for i in str:
        if i == 'M':
            return True
        else: return False