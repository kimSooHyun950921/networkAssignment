from node import node
class trie_node:
    def __init__(self,left_val=None,right_val=None,height=0,data=None):
        self.left = left_val
        self.right = right_val
        self.height = height
        self.data = data
    def left(self):
        if self.left == None:
            return None
        return self.left
    def right(self):
        if self.right == None:
            return None
        return self.right
    def height(self):
        return self.height
    def data(self):
        return self.data
    def set_left(self,left_val):
        self.left = left_val
    def set_right(self,right_val):
        self.right = right_val
    def set_height(self,height):
        self.height = height
    def set_data(self,data):
        self.data = data

    def __str__(self):
        if self.left != None and self.right!=None:
            return '\ncur:{'+str(self.data)+'}\nleft:{'+str(self.left.data)+' '+str(type(self.left))+'}\nright:{'+str(self.right.data)+' '+str(type(self.right))+'}'
        else:
            if self.left == None and self.right!=None:
                return '\ncur:{'+str(self.data)+'}\nleft:{'+str(self.left)+'}\nright:{'+str(type(self.right))+" right_value: "+str(self.right.data)+'}'
            elif self.left!=None and self.right==None: 
                return '\ncur:{'+str(self.data)+'}\nleft:{'+str(type(self.left))+"left_value:"+str(self.left.data)+'}\nright:{'+str(self.right)+'}'
            else:
                return '\ncur:{'+str(self.data)+'}\n left:{'+str(self.left)+'}\n right:{'+str(self.right)+'}'
                    



