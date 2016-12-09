

def correctify(string):
    ''' #Example string : b'test123' , returns test123
    :param string: Desired raw string
    :return: Valid string
    '''
    return string[2:-1]