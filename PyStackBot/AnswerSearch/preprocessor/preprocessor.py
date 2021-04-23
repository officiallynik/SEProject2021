import os
import re
from textblob import TextBlob
import software_tokenizer as tokenizer
import nltk
from nltk.stem import WordNetLemmatizer  # used for stemming
from remove_stopwords import remove_stopwords
nltk.download('punkt',quiet=True)
nltk.download('wordnet',quiet=True)


class PreprocessPostContent(object):
    """
    Contains relevant methods for Preprocessing Phase

    """

    code_snippet = re.compile(r"<pre>.*?</pre>")
    code_insider = re.compile(r"<code>.*?</code>")
    html_tag = re.compile(r"<.*?>")
    comment_bracket = re.compile(r"\(.*?\)")
    quotation = re.compile(r"(\'\')|(\")|(\`\`)")
    href_resource = re.compile(r"<a.*?>.*?</a>")
    paragraph = re.compile(r"<p>.*?</p>")
    equation1 = re.compile(r"\$.*?\$")
    equation2 = re.compile(r"\$\$.*?\$\$")
    integers = re.compile(r"^-?[1-9]\d*$")
    floats = re.compile(r"^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$")
    operators = re.compile(r"[><\+\-\*/=]")
    email = re.compile(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*")
    web_url = re.compile(r"[a-zA-z]+://[^\s]*")
    punctuation = re.compile("[,!?:#$%^&*\']")

    @staticmethod
    def filterNILStr(s):
        def filterFunc(s): return s and s.strip()
        s = ' '.join(filter(filterFunc, s.split())).strip()

        return s

    def __init__(self):
        self.max_quote_rate = 1.5
        self.max_quote_diff = 5
        self.min_words_sent = 5
        self.min_words_paragraph = 10
        self.max_number_pragraph = 5
        self.num_token = "[NUM]"
        self.code_token = "[CODE]"
        self.max_code = 5
        # lemmatize
        self.lemmatizer = WordNetLemmatizer()

    def remove_bracket(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:
            s = sent.string
            s_c = re.sub(self.comment_bracket, "", s)
            s_c_words = TextBlob(s_c).words
            if len(s_c_words) == 0 or len(sent.words) / len(s_c_words) > self.max_quote_rate or \
                    len(sent.words) - len(s_c_words) > self.max_quote_diff:
                continue
            cleaned.append(s_c)

        return " ".join(cleaned)

    def remove_quotation(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:
            s_c = re.sub(self.quotation, "", sent.string)
            cleaned.append(s_c)

        return " ".join(cleaned)

    def remove_href(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:
            s = sent.string
            s_c = re.sub(self.href_resource, "", s)
            if sent.words != TextBlob(s_c).words:
                continue
            cleaned.append(s)

        return " ".join(cleaned)

    def remove_code(self, txt):
        cleaned = re.sub(self.code_snippet, "", txt)
        return cleaned

    def remove_equation(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:
            s = sent.string
            s_c = re.sub(self.equation2, "", s)
            s_c = re.sub(self.equation1, "", s_c)
            if sent.words != TextBlob(s_c).words:
                continue
            cleaned.append(s)

        return " ".join(cleaned)

    def remove_numbers(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:

            s_tokens = sent.string.split()
            
            s_tokens = list(
                map(lambda t: re.sub(self.floats, "", t), s_tokens))
            
            s_tokens = map(lambda t: re.sub(self.integers, "", t), s_tokens)
            s_c = " ".join(s_tokens)
           

            if len(sent.words) - len(TextBlob(s_c).words) > self.max_number_pragraph:
                continue

            s_tokens = sent.string.split()
            s_tokens = map(lambda t: re.sub(self.floats, " %s " %
                                            self.num_token, t), s_tokens)
            s_tokens = map(lambda t: re.sub(self.integers, " %s " %
                                            self.num_token, t), s_tokens)
            s_c = " ".join(s_tokens)

            cleaned.append(s_c)

        cleaned = " ".join(cleaned)

        return cleaned

    def remove_operators(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:
            s = sent.string
            s_c = re.findall(self.operators, s)
            if len(s_c) > 3:
                continue
            cleaned.append(s)

        return " ".join(cleaned)

    def remove_hmtltag(self, txt):
        cleaned = re.sub(self.html_tag, "", txt)
        return cleaned

    def remove_email(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:
            s = sent.string
            s_c = re.sub(self.email, "", s)
            if sent.words != TextBlob(s_c).words:
                continue
            cleaned.append(s)
        return " ".join(cleaned)

    def remove_url(self, txt):
        cleaned = []
        for sent in TextBlob(txt).sentences:
            s = sent.string
            s_c = re.sub(self.web_url, "", s)
            if sent.words != TextBlob(s_c).words:
                continue
            cleaned.append(s)
        return " ".join(cleaned)

    def remove_useless(self, txt):
        cleaned = []

        for sent in TextBlob(txt).sentences:
            
            if len(sent.words) < self.min_words_sent:
                continue
            if sent[-1] not in ('.', '?', '!') and len(sent.words) < 2 * self.min_words_sent:
                continue
            cleaned.append(sent.string)

        return " ".join(cleaned)

    def remove_punctuation(self, txt):
        cleaned = re.sub(self.punctuation, "", txt)
        return cleaned

    def __process(self, txt):

        

        txt = self.remove_href(txt)
        

        txt = self.remove_email(txt)
        

        txt = self.remove_url(txt)
        

        txt = self.remove_hmtltag(txt)
        

        txt = self.remove_equation(txt)
        

        txt = self.remove_bracket(txt)
        

        txt = self.remove_numbers(txt)
        

        txt = self.remove_operators(txt)
        

        txt = self.remove_quotation(txt)

        return txt

    def getParagraphs(self, raw_txt):
        raw_txt = self.filterNILStr(raw_txt)
        paragraphs_candidates = re.findall(self.paragraph, raw_txt)
        # paragraphs_candidates = [p[3:-4]
        #                          for p in paragraphs_candidates if len(p[3:-4]) > 0]
        paragraphs = []
        for p in paragraphs_candidates:
            if len(TextBlob(p).words) < self.min_words_paragraph:
                continue
            paragraphs.append(p)
        return paragraphs

    def filter_wordlist(self, wordlist):
        def condition(t): return len(t) > 1 or t.upper() == 'I'
        filter_list = list(filter(condition, wordlist))
        return filter_list

    def lemmatize(self, text):
        text = [self.lemmatizer.lemmatize(token) for token in text]
        return text

    # [ [word1, word2, ...], [word1, word2, ...], [word1, word2, ...], ... ]
    def get_mul_para_wordlist_list(self, raw_txt):
        # return a list of paragraphs of plain text(word list)
        raw_txt = raw_txt.lower()
        txt = self.remove_code(raw_txt)

        paragraphs = self.getParagraphs(txt)

        wordlist_list = []
        for p in paragraphs:
            cleaned = self.__process(p)
            if len(cleaned.split()) == 0:
                continue

            wordlist = self.filterNILStr(cleaned)
            wordlist = tokenizer.tokenize(wordlist)
            wordlist = self.filter_wordlist(wordlist)
            
            wordlist = remove_stopwords(wordlist)
            
            wordlist = self.lemmatize(wordlist)
            
            wordlist_list.append(' '.join(wordlist))

        return ' '.join(wordlist_list)

    # [word1, word2, ...]
    def get_single_para_word_list(self, raw_txt):
        # return a list of plain text(word list)
        # filter code
        raw_txt = raw_txt.lower()

        cleaned = self.__process(raw_txt)

        text = self.filterNILStr(cleaned)

        word_list = tokenizer.tokenize(text)

        word_list = self.filter_wordlist(word_list)

        word_list = remove_stopwords(word_list)

        word_list = self.lemmatize(word_list)
       
        return ' '.join(word_list)


if __name__ == '__main__':
    
    ans = '''
        <p>It is saied that Whenever<code>code</code> a problem becomes solvable by a computer, people start arguing that it does not require intelligence . </p>
        <p>[CLS] "Whenever a problem becomes solvable by a computer , people start arguing that it does not require intelligence . [SEP] John McCarthy is often quoted : `` As soon as it works , no one calls it AI anymore '' ( Referenced in CACM )[SEP] ."</p>

        <p>"One of my teachers in <code>jet.listen</code>college said that in the 1950 's , a professor was asked what he thought was intelligent for a machine . The professor reputedly answered that if a vending machine gave him the right change , that would be intelligent ."</p>

        <p>"Later , playing chess was considered intelligent . However , computers can now defeat grandmasters at chess , and people are no longer saying that it is a form of intelligence ."</p>

        <p>"Now we have OCR . It 's already stated in another answer that our methods do not have the recognition facilities of a 5 year old . As soon as this is achieved , people will say `` meh , that 's not intelligence , a 5 year old can do that ! ''"</p>

        <p>"A psychological bias , a need to state that we are somehow superior to machines , is at the basis of this ."</p>
    '''
    answer = PreprocessPostContent().get_mul_para_wordlist_list(ans)
    