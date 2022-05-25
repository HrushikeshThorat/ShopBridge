'''
    Exceptions
'''

class InvalidInputException(Exception):
    def __init__(self):
        self.description = 'Invalid value! Please fill proper value.'
                
class WrongInputException(Exception):
    def __init__(self):
        self.description = '''Wrong Product_Id! Product with this Product_Id doesn't exist.'''