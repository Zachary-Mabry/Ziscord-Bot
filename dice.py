from random import randint

def parse_roll(s):
    s = s.replace(' ', '')
    numrolls = s.count('d')
    res = []
    for i in range(0, numrolls):
        dice = int(s[0:s.index('d')])
        s = s[s.index('d')+1:]
        if s.find("+") != -1:
            hi = int(s[0:s.index('+')])
            s = s[s.index('+')+1:]
        else:
            if s.find("+") == -1:
                hi = int(s)
                s = ""
            else:
                s = s[s.find('+')+1:]
        res.append(roll(dice, hi))
    if len(s) > 0:    
        res.append([int(s)])
    return format_result(res)

def roll(numdice, hival):
    print("-----")
    print(numdice)
    print(hival)
    print("-----")
    res = []
    for i in range(0, numdice):
        res.append(randint(1, hival))
    return res

def format_result(res):
    s = 0
    for i in range(0, len(res)):
        s += sum(res[i])
    out = "You rolled **" + str(s) + "**! Details: "
    for i in range(0, len(res)):
        out += "( "
        for j in range(0, len(res[i])):
            out += str(res[i][j])
            if j != len(res[i]) - 1:
                out += " + "
            else:
                out += " )"
        if i != len(res) - 1:
            out += " + "
        else:
            out += ""
    return out
