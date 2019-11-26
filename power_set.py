def p(s):
    if s==[]: # base case
        return [s] # if s is empty, then the only sublist of s is s itself
    else:
        e = s[0] # any element from s (in this implementation, we choose the first element)
        t = s[1:] # s with e removed
        pt = p(t) # the list of all sublists of t (note that this is a recursive call)
        fept = [x + [e] for x in pt] # pt with e appended to each sublist
        return pt + fept # the concatenation of all constructed sublists

# example:
print(p(['x', 'y', 'z']))