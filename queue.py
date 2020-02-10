  
# A linked list node
# to store a queue entry 
class Node: 
      
    def __init__(self, data): 
        self.data = data 
        self.next = None
  
# The front of the queue stores the front node
# of linked list and rear stores the last node of linked list
class Queue: 
      
    def __init__(self): 
        self.front = self.rear = None
  
    def isEmpty(self): 
        return self.front == None
      
    def enqueue(self, item):
        temp = Node(item) 
          
        if self.rear == None: 
            self.front = self.rear = temp 
            return
        self.rear.next = temp 
        self.rear = temp 
  
    def dequeue(self):
          
        if self.isEmpty(): 
            return
        temp = self.front 
        self.front = temp.next
        
        if(self.front == None): 
            self.rear = None
        return temp.data    
