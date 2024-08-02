from Dictionary import Dictionary

def stringify_stack(lst, printStackParanthesis=False):
    if lst == []:
        return "[ ]"
    s = ' '.join(stringify_stack(item, True) if isinstance(item, list) else str(item) for item in lst)
    if printStackParanthesis == True:
        if isinstance(lst, Dictionary):
            s = "{ "+s+" }"
        else:
            s = "[ "+s+" ]"
    return s
