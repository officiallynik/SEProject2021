"""
    Contains relevant methods for tokenization during preprocessing phase

"""


import re
import sys
import emoticons as emoticons


def mycompile(pat): return re.compile(pat, re.UNICODE)


def regex_or(*items):
    r = '|'.join(items)
    r = '(' + r + ')'
    return r


def pos_lookahead(r):
    return '(?=' + r + ')'


def neg_lookahead(r):
    return '(?!' + r + ')'


def optional(r):
    return '(%s)?' % r


PunctChars = r'''['“".?!,(/:;]'''
foo = r'''foo'''
Punct = '%s+' % PunctChars
PunctSeq = r"""['`\"“”‘’)]+|[.?!,…]+|[:;/(]+"""
Entity = '&(amp|lt|gt|quot);'

# more complex version:
UrlStart1 = regex_or('https?://', r'www\.')
CommonTLDs = regex_or('com', 'co\\.uk', 'org', 'net',
                      'info', 'ca', 'edu', 'gov')
UrlStart2 = r'[a-z0-9\.-]+?' + r'\.' + CommonTLDs + pos_lookahead(r'[/ \W\b]')
# * not + for case of:  "go to bla.com." -- don't want period
UrlBody = r'[^ \t\r\n<>]*?'
UrlExtraCrapBeforeEnd = '%s+?' % regex_or(PunctChars, Entity)
UrlEnd = regex_or(r'\.\.+', r'[<>]', r'\s', '$')  # / added by Deheng

Url = (r'\b' +
       regex_or(UrlStart1, UrlStart2) +
       UrlBody +
       pos_lookahead(optional(UrlExtraCrapBeforeEnd) + UrlEnd))

Url_RE = re.compile("(%s)" % Url, re.U | re.I)

EmailName = r'([a-zA-Z0-9-_+]+[.])*[a-zA-Z0-9-_+]+'
EmailDomain = r'([a-zA-Z0-9]+[.])+' + CommonTLDs
Email = EmailName + "@" + EmailDomain

Email_RE = mycompile(Email)

API = regex_or(r'((\w+)\.)+\w+\(\)', r'\w+\(\)', r'((\w+)\.)+(\w+)')
API_RE = mycompile(API)
plural = r'\w+\(s\)'
plural_RE = mycompile(plural)
ProgrammingOperators = regex_or(r'==', r'!=', r'>=', r'<=', r'&&', r'\|\|')

Concat = r'\w+[/—]\w+'

Timelike = r'\d+:\d+'
NumNum = r'\d+\.\d+'
NumberWithCommas = r'(\d+,)+?\d{3}' + pos_lookahead(regex_or('[^,]', '$'))

Abbrevs1 = ['am', 'pm', 'us', 'usa', 'ie', 'eg']


def regexify_abbrev(a):
    chars = list(a)
    icase = ["[%s%s]" % (c, c.upper()) for c in chars]
    dotted = [r'%s\.' % x for x in icase]
    return "".join(dotted)


Abbrevs = [regexify_abbrev(a) for a in Abbrevs1]

BoundaryNotDot = regex_or(r'\s', '[“"?!,:;]', Entity)
aa1 = r'''([A-Za-z]\.){2,}''' + pos_lookahead(BoundaryNotDot)
aa2 = r'''([A-Za-z]\.){1,}[A-Za-z]''' + pos_lookahead(BoundaryNotDot)
ArbitraryAbbrev = regex_or(aa1, aa2)

assert '-' != '―'
Separators = regex_or('--+', '―')
Decorations = r' [  ♫   ]+ '.replace(' ', '')

EmbeddedApostrophe = r"\S+'\w+"  # \S -> \w, by Deheng

Hashtag = r'#[a-zA-Z0-9_]+'

AtMention = r'@[a-zA-Z0-9_]+'

ProtectThese = [
    emoticons.Emoticon,
    Url,
    Email,
    Entity,
    Hashtag,
    AtMention,
    Timelike,
    NumNum,
    NumberWithCommas,
    ArbitraryAbbrev,
    Separators,
    Decorations,
    EmbeddedApostrophe,
    API,  
    PunctSeq,  
    plural,  
    ProgrammingOperators  
]
Protect_RE = mycompile(regex_or(*ProtectThese))


class Tokenization(list):
    " list of tokens, plus extra info "

    def __init__(self):
        self.alignments = []
        self.text = ""

    def subset(self, tok_inds):
        new = Tokenization()
        new += [self[i] for i in tok_inds]
        new.alignments = [self.alignments[i] for i in tok_inds]
        new.text = self.text
        return new

    def assert_consistent(t):
        assert len(t) == len(t.alignments)
        assert [t.text[t.alignments[i]: (t.alignments[i] + len(t[i]))]
                for i in range(len(t))] == list(t)


def align(toks, orig):
    s_i = 0
    alignments = [None] * len(toks)
    for tok_i in range(len(toks)):
        while True:
            L = len(toks[tok_i])
            if orig[s_i:(s_i + L)] == toks[tok_i]:
                alignments[tok_i] = s_i
                s_i += L
                break
            s_i += 1
            if s_i >= len(orig):
                raise AlignmentFailed((orig, toks, alignments))
            
    if any(a is None for a in alignments):
        raise AlignmentFailed((orig, toks, alignments))

    return alignments


class AlignmentFailed(Exception):
    pass


def tokenize(tweet):
    
    text = tweet
    text = re.sub(u'—', ' ', text)  
    text = re.sub('(?<=\w)/(\s|$)', ' ', text)  
    text = squeeze_whitespace(text)
    # Convert HTML escape sequences into their actual characters (so that the tokenizer and emoticon finder are not fooled).
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&amp;', '&', text)

    t = Tokenization()
    t += simple_tokenize(text)
    t.text = text
    t.alignments = align(t, text)
    return t


def simple_tokenize(text):
    s = text
    s = edge_punct_munge(s)

    # strict alternating ordering through the string.  first and last are goods.
    # good bad good bad good bad good
    goods = []
    bads = []
    i = 0
    if Protect_RE.search(s):
        for m in Protect_RE.finditer(s):
            goods.append((i, m.start()))
            bads.append(m.span())
            i = m.end()
        goods.append((m.end(), len(s)))
    else:
        goods = [(0, len(s))]
    assert len(bads) + 1 == len(goods)

    goods = [s[i:j] for i, j in goods]
    bads = [s[i:j] for i, j in bads]
    goods = [unprotected_tokenize(x) for x in goods]
    res = []
    for i in range(len(bads)):
        res += goods[i]
        res.append(bads[i])
    res += goods[-1]
    return res


AposS = mycompile(r"(\S+)('s)$")


def post_process(pre_toks):
    # hacky: further splitting of certain tokens
    post_toks = []
    for tok in pre_toks:
        m = AposS.search(tok)
        if m:
            post_toks += m.groups()
        else:
            post_toks.append(tok)
    return post_toks


WS_RE = mycompile(r'\s+')


def squeeze_whitespace(s):
    new_string = WS_RE.sub(" ", s)
    return new_string.strip()



EdgePunct = r"""[  ' " “ ” ‘ ’ * « » { } ( \) [ \]  ]""".replace(' ', '')
NotEdgePunct = r"""[a-zA-Z0-9]"""
EdgePunctLeft = r"""(\s|^)(%s+)(%s)""" % (EdgePunct, NotEdgePunct)

# programming API suffixes () are considered
EdgePunctRight = r"""(%s(?:\(s?\))?)(%s*)(\s|$)""" % (NotEdgePunct, EdgePunct)
EdgePunctLeft_RE = mycompile(EdgePunctLeft)
EdgePunctRight_RE = mycompile(EdgePunctRight)


def edge_punct_munge(s):
    s = EdgePunctLeft_RE.sub(r"\1\2 \3", s)
    s = EdgePunctRight_RE.sub(r"\1 \2\3", s)
    return s


def unprotected_tokenize(s):
    return s.split()


if __name__ == '__main__':
    s = "What’s the equivalent of Carbon.ControlAccessor() in python __init__?"
    print(tokenize(s))