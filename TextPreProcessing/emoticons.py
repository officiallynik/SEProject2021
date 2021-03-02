# emoticon recognition via patterns.

"""Author: Brendan O'Connor (brenocon.com, brenocon@gmail.com)"""
"""Modified for part-of-speech tagging by Kevin Gimpel (kgimpel@cs.cmu.edu) and Daniel Mills (dpmills@cs.cmu.edu)"""


import sys
import re
import sane_re
def mycompile(pat): return re.compile(pat,  re.UNICODE)


NormalEyes = r'[:=8]'
Wink = r'[;]'

NoseArea = r'(|o|O|-)'

HappyMouths = r'[D\)\]]'
SadMouths = r'[\(\[]'
Tongue = r'[pPb]'
OtherMouths = r'[\|doO/\\]'

Happy_RE = mycompile('(\^_\^|' + NormalEyes + NoseArea + HappyMouths + ')')
Sad_RE = mycompile(NormalEyes + NoseArea + SadMouths)

Wink_RE = mycompile(Wink + NoseArea + HappyMouths)
Tongue_RE = mycompile(NormalEyes + NoseArea + Tongue)
Other_RE = mycompile('('+NormalEyes+'|'+Wink+')' + NoseArea + OtherMouths)


Faces = (
    "(" +
    "("+NormalEyes+"|"+Wink+")" +
    NoseArea +
    "("+Tongue+"|"+OtherMouths+"|"+SadMouths+"+|"+HappyMouths+"+)" +
    "|" +
    "("+SadMouths+"+|"+HappyMouths+"+)" +
    NoseArea +
    "("+NormalEyes+"|"+Wink+")" +
    ")"
)

Hearts = r'(<+/?3+)'

Arrows = r'(<*[-=]*>+|<+[-=]*>*)'

Emoticon = "("+Hearts+"|"+Faces+"|"+Arrows+")"

Emoticon_RE = mycompile(Emoticon)


def analyze_text(text):
    h = Happy_RE.search(text)
    s = Sad_RE.search(text)
    if h and s:
        return "BOTH_HS"
    if h:
        return "HAPPY"
    if s:
        return "SAD"
    return "NA"

    # more complex & harder, so disabled for now
    #w= Wink_RE.search(text)
    #t= Tongue_RE.search(text)
    #a= Other_RE.search(text)
    #h,w,s,t,a = [bool(x) for x in [h,w,s,t,a]]
    # if sum([h,w,s,t,a])>1: return "MULTIPLE"
    # if sum([h,w,s,t,a])==1:
    #  if h: return "HAPPY"
    #  if s: return "SAD"
    #  if w: return "WINK"
    #  if a: return "OTHER"
    #  if t: return "TONGUE"
    # return "NA"


if __name__ == '__main__':
    for line in sys.stdin:
        sane_re._S(line[:-1]).show_match(Emoticon_RE, numbers=False)
        #print(analyze_tweet(line.strip()), line.strip(), sep="\t")
