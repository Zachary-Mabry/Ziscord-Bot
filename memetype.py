def meme(s):
    count = 0
    outl = []
    out = ""
    numdict = {'1':'one', '2':'two', '3':'three', '4':'four', '5':'five', '6':'six', '7':'seven', '8':'eight',
               '9':'nine', '0':'zero'}
    while count < len(s):
        if not s[count].isalnum():
            if s[count] == " ":
                out += "    "
            else:
                out += s[count]
            count += 1
        else:
            if numdict.__contains__(s[count]):
                out += ":" + numdict[s[count]] + ": "
                count += 1
            else:
                out += ":regional_indicator_" + s[count].lower() + ": "
                count += 1
        if len(out) > 1970:
            outl.append(out)
            out = ""
    outl.append(out)
    return outl
meme("hello 1234")