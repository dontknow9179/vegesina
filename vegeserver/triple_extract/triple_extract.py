import re
from triple_extract.pyltp_function import *

class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()
    
    '''文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识'''
    def split_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；;：:\n\r]', content) if sentence]
    
    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''
    def srl(self, words, postags, roles_dict):
        svos = []
        for index in range(len(postags)):
            if index in roles_dict:
                v = words[index]
                role_info = roles_dict[index]
                if 'A0' in role_info.keys() and 'A1' in role_info.keys():
                    s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2]+1) if
                                 postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
                    o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
                                 postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
                    if s and o:
                        # return '1', [s, v, o]
                        svos.append([s, v, o])
                # elif 'A0' in role_info:
                #     s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
                #                  postags[word_index][0] not in ['w', 'u', 'x']])
                #     if s:
                #         # return '2', [s, v, '']
                #         svos.append([s, v, ''])
                # elif 'A1' in role_info:
                #     o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
                #                  postags[word_index][0] not in ['w', 'u', 'x']])
                #     # return '3', ['', v, o]
                #     svos.append(['', v, o])
                # # return '4', []
        return svos


    def dp_vege(self, words, postags, child_dict_list, arcs, roles_dict, article_id):
        svos = []
        for index in range(len(postags)):
            # 如果语义角色标记为空，则使用依存句法进行抽取
            # if postags[index] == 'v':
            if postags[index]:              # 这里返回的词都是子元素的，而且不一定是动词
                # 抽取以谓词为中心的事实三元组
                # print("words:{}".format(words[index]))
                child_dict = child_dict_list[index]
                # print("child_dict:{}".format(child_dict))
                # 主谓宾
                if 'SBV' in child_dict and 'VOB' in child_dict:
                    r = words[index]
                    e1 = words[child_dict['SBV'][0]]
                    e2 = words[child_dict['VOB'][0]]
                    svo = {}
                    svo['s'] = e1
                    svo['v'] = r
                    svo['o'] = e2
                    svo['article_id'] = article_id
                    svos.append(svo)
                elif 'SBV' in child_dict and 'VOB' not in child_dict:
                    r = words[index]
                    e1 = words[child_dict['SBV'][0]]
                    svo = {}
                    svo['s'] = e1
                    svo['v'] = r
                    svo['o'] = ''
                    svo['article_id'] = article_id
                    svos.append(svo)
                elif 'SBV' not in child_dict and 'VOB' in child_dict:
                    r = words[index]
                    e2 = words[child_dict['VOB'][0]]
                    svo = {}
                    svo['s'] = ''
                    svo['v'] = r
                    svo['o'] = e2
                    svo['article_id'] = article_id
                    svos.append(svo)
        return svos


    def dp(self, words, postags, child_dict_list, arcs, roles_dict):
        svos = []
        for index in range(len(postags)):

            # 如果语义角色标记为空，则使用依存句法进行抽取
            # if postags[index] == 'v':
            if postags[index]:              # 这里返回的词都是子元素的，而且不一定是动词
                # 抽取以谓词为中心的事实三元组
                # print("words:{}".format(words[index]))
                child_dict = child_dict_list[index]
                # print("child_dict:{}".format(child_dict))
                # 主谓宾
                if 'SBV' in child_dict and 'VOB' in child_dict:
                    r = words[index]
                    # e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                    e1 = words[child_dict['SBV'][0]]
                    # e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                    e2 = words[child_dict['VOB'][0]]
                    svos.append([e1, r, e2])
                elif 'SBV' in child_dict and 'VOB' not in child_dict:
                    r = words[index]
                    # e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                    e1 = words[child_dict['SBV'][0]]
                    svos.append([e1, r, ''])
                elif 'SBV' not in child_dict and 'VOB' in child_dict:
                    r = words[index]
                    # e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                    e2 = words[child_dict['VOB'][0]]
                    svos.append(['', r, e2])

                # # 定语后置，动宾关系
                # relation = arcs[index][0]
                # head = arcs[index][2]
                # if relation == 'ATT':
                #     if 'VOB' in child_dict:
                #         e1 = self.complete_e(words, postags, child_dict_list, head - 1)
                #         r = words[index]
                #         e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                #         temp_string = r + e2
                #         if temp_string == e1[:len(temp_string)]:
                #             e1 = e1[len(temp_string):]
                #         if temp_string not in e1:
                #             svos.append([e1, r, e2])
                # # 含有介宾关系的主谓动补关系
                # if 'SBV' in child_dict and 'CMP' in child_dict:
                #     e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                #     cmp_index = child_dict['CMP'][0]
                #     r = words[index] + words[cmp_index]
                #     if 'POB' in child_dict_list[cmp_index]:
                #         e2 = self.complete_e(words, postags, child_dict_list,
                #                              child_dict_list[cmp_index]['POB'][0])
                #         svos.append([e1, r, e2])

        return svos

    '''对找出的主语或者宾语进行扩展'''
    def complete_e(self, words, postags, child_dict_list, word_index):
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix + words[word_index] + postfix


    def triples_main_vege(self, content, article_id, sentence_count=1):
        """
        对输入的文本，进行三元组提取
        :param content: 输入文本，可以为多个句子
        :param sentence_count: 中心句的个数，默认为1
        :return: SPO三元组列表
        """
        sentences = self.split_sents(content)
        svos = []
        for i, sentence in enumerate(sentences):
            if i < sentence_count:
                words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentence)
                svo = self.dp_vege(words, postags, child_dict_list, arcs, roles_dict, article_id)
                svos += svo
        return svos


    '''程序主控函数'''
    def triples_main(self, content, method='dp'):
        """
        对输入的文本，进行三元组提取
        :param content: 输入文本，可以为多个句子
        :param method: 使用的方法，取值为'dp'或者'srl'，默认使用dp，即依存句法分析，可以选用srl，即语义角色分析
        :return: SPO三元组列表
        """
        sentences = self.split_sents(content)
        svos = []
        if method == 'dp':
            for sentence in sentences:
                words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentence)
                svo = self.dp(words, postags, child_dict_list, arcs, roles_dict)
                svos += svo
        elif method == 'srl':
            for sentence in sentences:
                words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentence)
                svo = self.srl(words, postags, roles_dict)
                if not svo:
                    svo = self.dp(words, postags, child_dict_list, arcs, roles_dict)
                svos += svo
        return svos

extractor = TripleExtractor()
# svos = extractor.triples_main('景甜疑似与张继科分手, 男方已洗掉纹身, 预计年前官宣!',method='srl')
# print(svos)

class TripleTest(TestCase):

    def test_triple(self):
        content5 = ''' 以色列国防军20日对加沙地带实施轰炸，造成3名巴勒斯坦武装人员死亡。此外，巴勒斯坦人与以色列士兵当天在加沙地带与以交界地区发生冲突，一名巴勒斯坦人被打死。当天的冲突还造成210名巴勒斯坦人受伤。
            当天，数千名巴勒斯坦人在加沙地带边境地区继续“回归大游行”抗议活动。部分示威者燃烧轮胎，并向以军投掷石块、燃烧瓶等，驻守边境的以军士兵向示威人群发射催泪瓦斯并开枪射击。'''
        text = '刚刚，埃塞俄比亚航空集团CEO抵达飞机坠毁现场，确认无乘客生还，从埃航推特上发布的照片看，航班残片遍地都是'
        extractor = TripleExtractor()
        text1 = '国务院总理李克强调研上海外高桥时提出，支持上海积极探索新机制。'
        # svos = extractor.triples_main("古天乐48岁还未结婚，现两人都48岁了，还不准备公开吗？")
        # svos = extractor.triples_main(text1, method='dp')
        # svos = extractor.triples_main('景甜疑似与张继科分手, 男方已洗掉纹身, 预计年前官宣!', method='dp') # -> [['景甜', '疑似', '分手'], ['男方', '洗', '纹身'], ['', '预计', '官宣']]
        # svos = extractor.triples_main('景甜惊爆分手！4天前松口：享受孤独！张继科传“洗掉定情刺青”', method='dp')
        svos = extractor.triples_main('邓紫棋因演唱会延迟发文道歉并90度鞠躬道歉', method='dp')
        print('svos', svos)