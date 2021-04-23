"""
emoticon recognition via patterns.

"""
import sys
import re

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
