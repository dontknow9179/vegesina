import re
from pyltp_function import *

class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()
    
    '''文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识'''
    def split_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；;：:\n\r]', content) if sentence]

extractor = TripleExtractor()