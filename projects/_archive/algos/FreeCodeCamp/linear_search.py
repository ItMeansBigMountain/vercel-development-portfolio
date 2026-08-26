def linear_search(list, target):
    for x in range(0,len(list), 1):
        if target == list[x]:
            return x
    return None




numbers = [x for x in range(0,100,5)]
target = 15
search_index = linear_search(numbers , 15 )
print(numbers)
print(search_index)