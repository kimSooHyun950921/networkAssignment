class node:
    def __init__(self, new_next_hop=None):
        self.__next_hop = new_next_hop
    def next_hop(self):
        return self.__next_hop
    def set_next_hop(self,new_next_hop):
        self.__next_hop = new_next_hop
    def __str__(self):
        if self.next_hop() is None:
            return "None"
        return str(self.next_hop())
