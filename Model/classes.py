class User: 
    def __init__(self, username, password, confirmation='n/a'):
        """
        :type username: string
        :type password: string
        """
        self.username = username    
        self.password = password
        self.confirmation = confirmation
