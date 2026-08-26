def longestCommonPrefix( strs ) :
    # init
    output = ""
    valid = True
    str_index = 0

    if len(strs) < 2 :
        return strs[0]
    while valid:
        if strs[0] == "":
            return strs[0]

        test = strs[0][str_index]
        for x in range(1 , len(strs) , 1):
            if len(strs[x]) < str_index + 1:
                valid = False
            elif strs[x][str_index] != test:
                valid = False
        if valid:
            output += test
        
        if str_index + 1 < len(strs[0]) :
            str_index += 1
        else:
            valid = False

    return output











out = longestCommonPrefix( ["flower","flower","flower","flower"] )
print(out)