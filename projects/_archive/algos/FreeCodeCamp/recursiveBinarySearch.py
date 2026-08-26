def recursive_binary_search(list , target):
    if len(list) == 0 : return False
    midpoint = len(list) // 2
    if list[midpoint] == target:
        return True
    elif list[midpoint] < target:
        return recursive_binary_search(list[midpoint+1:], target)
    elif list[midpoint] > target:
        return recursive_binary_search(list[:midpoint], target)




numbers = [x for x in range(0,100,5)]
target = 15
search_index = recursive_binary_search(numbers ,15)
print(numbers)
print(search_index)