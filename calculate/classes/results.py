

class SpecialNodeFinal(dict):

    def __init__(self, **kwargs):
        self.quantity = 0
        self.type = "default"
        super().__init__(**kwargs)
