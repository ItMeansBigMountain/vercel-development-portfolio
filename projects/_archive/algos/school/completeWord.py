def can_complete(initial, word):
    valid = False
    par = []
    start = 0
    for l in range(  0  , len(initial) , 1   ):
        print("-------------")
        found = False

        for i in range( start , len(word) , 1 ):
            if word[i] == initial[l]:
                word = word[0:i] + ' ' + word[i + 1:]
                check_last = 0
                for z in range( l+1  , len(initial) , 1  ):
                    check_last += 1
                    for p in range( 0 , len(word) , 1 ):
                        if word[p] == initial[z]:
                            if i < p:
                                found = True
                if check_last < 1:
                    found = True

        start += 1
        if found:
            par.append(True)
        else:
            par.append(False)
    
    print(par)
    if False in par:
        return False
    else:
        return True








output = can_complete('siing', 'something')

print(output)