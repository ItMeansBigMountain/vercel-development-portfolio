class Node:
    data = None
    next_node = None

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"<{self.data}>"


class LinkedList:
    def __init__(self):
        self.head = None
    
    def isEmpty(self):
        return self.head == None
    
    def size(self):
        count = 0
        current_node = self.head
        while current_node != None:
            count += 1
            current_node = current_node.next_node
        return count

    def add(self, data):
        new_node = Node(data)
        new_node.next_node = self.head
        self.head = new_node

    def insert(self, data , index):
        current_node = self.head
        position = 0

        if index > self.size(): return None
        while current_node != None:
            if position == index-1:
                new_node = Node(data)
                new_node.next_node = current_node.next_node
                current_node.next_node = new_node
                break
            position += 1
            current_node = current_node.next_node

    def removeByKey(self, key):
        current_node = self.head
        previous_node = None
        while current_node != None :
            if key == current_node.data and current_node is self.head :
                self.head = current_node.next_node
                return current_node
            elif key == current_node.data and current_node is not self.head :
                previous_node.next_node = current_node.next_node
                return current_node
            else:
                previous_node = current_node
                current_node = current_node.next_node
        return None

    def removeByIndex(self, index):
        current_node = self.head
        position = 0

        if index > self.size(): return None
        if index == 0: self.head = self.head.next_node
        while current_node != None:
            if position == index-1:
                target = current_node.next_node
                current_node.next_node = target.next_node
                return current_node
            position += 1
            current_node = current_node.next_node
        return None

    def searchByKey(self, key):
        current_node = self.head
        index = 0
        while current_node != None:
            if current_node.data == key:
                return index
            index += 1
            current_node = current_node.next_node
        return None

    def searchByIndex(self, index):
        current_node = self.head
        position = 0
        while current_node != None:
            if position == index:
                return current_node.data
            position += 1
            current_node = current_node.next_node
        return None

    def __repr__(self):
        output = ""
        current_node = self.head
        while current_node != None:
            if current_node.next_node:
                output += f"{current_node} -> "
            else:
                output += f"{current_node}"
            current_node = current_node.next_node
        return output







if __name__ == "__main__":
    # Showcasing methods down here
    l = LinkedList()



    print("\nADDING TO LINKED LIST...")
    l.add(10)
    l.add(20)
    l.add(30)
    l.add(40)
    print(l)
    print("size:", l.size())


    
    print("\nSEARCHING LINKED LIST BY VALUE...")
    s = 10
    found_index =  l.searchByKey(s)
    print(f"Found node value {s} at index: {found_index}")

    
    print("\nSEARCHING LINKED LIST BY INDEX...")
    i = 3
    found_value =  l.searchByIndex(i)
    print(f"Found node index {i} as value: {found_value}")



    print("\nINSERTED INTO LINKED LIST...")
    l.insert(3,3)
    l.insert(3,3)
    l.insert(3,3)
    l.insert(3,3)
    l.insert(3,3)
    l.insert(3,3)
    print(l)
    print("size:", l.size())



    print("\nREMOVING FROM LINKED LIST BY INDEX (looped)...")
    for x in range(5): l.removeByIndex(x)
    print(l)
    print("size:", l.size())



    print("\nREMOVING FROM LINKED LIST BY VALUE...")
    l.removeByKey(3)
    print(l)
    print("size:", l.size())
