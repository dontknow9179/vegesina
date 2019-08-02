import os

from django.test import TestCase
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller


class LtpParser:
    def __init__(self):
        LTP_DIR = '../../EventTriplesExtraction/ltp_data_v3.4.0'
        print(LTP_DIR)
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl_win.model'))

    '''语义角色标注'''
    def format_labelrole(self, words, postags):
        arcs = self.parser.parse(words, postags)
        roles = self.labeller.label(words, postags, arcs)
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name:[arg.name,arg.range.start, arg.range.end] for arg in role.arguments}
            # role.index 代表谓词的索引，从0开始
            # role.arguments 代表关于该谓词的若干语义角色：
            #   其中arg.name 表示语义角色内容，arg.range.start 表示语义角色起始词的位置的索引，arg.range.end 表示语义角色结束词的位置的索引
        return roles_dict

    '''句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典'''
    def build_parse_child_dict(self, words, postags, arcs):
        child_dict_list = []
        format_parse_list = []
        # 依存句法分析结果中，对应的每个词只记录了一个依存弧
        # 其中ROOT结点的索引是0，第一个词开始的索引依次为1、2、3
        # arc.head 表示依存弧的父节点词的索引。
        # arc.relation 表示依存弧的关系。
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                # 因为要记录这个结点的所有子结点，弧的head属性记录的是父结点的索引，所以遍历记录head值为该结点的点即为子结点
                if arcs[arc_index].head == index+1:   #arcs的索引从1开始
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)
        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id（head属性记录的是是父结点的索引）
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            # ['ATT', '李克强', 0, 'nh', '总理', 1, 'n']
            # 格式化依存关系，方便后续处理，
            # 分别表示：单词的依存关系，单词，单词下标，单词词性，单词父结点的单词，单词父结点的单词的下标，单词父结点的单词的词性
            a = [relation[i], words[i], i, postags[i], heads[i], rely_id[i]-1, postags[rely_id[i]-1]]
            format_parse_list.append(a)

        return child_dict_list, format_parse_list


    def get_verbs(self, content):
        words = list(self.segmentor.segment(content))
        postags = list(self.postagger.postag(words))
        verbs = []
        for index, postag in enumerate(postags):
            if postag == 'v':
                verbs.append(words[index])
        return verbs


    def get_entities(self, content):
        words = list(self.segmentor.segment(content))
        postags = list(self.postagger.postag(words))
        entities = []
        for index, postag in enumerate(postags):
            if postag == 'nh':
                entities.append(words[index])
        return entities


    '''parser主函数'''
    def parser_main(self, sentence):
        words = list(self.segmentor.segment(sentence))
        postags = list(self.postagger.postag(words))
        arcs = self.parser.parse(words, postags)
        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        roles_dict = self.format_labelrole(words, postags)
        return words, postags, child_dict_list, roles_dict, format_parse_list

parse = LtpParser()
sentence = '李克强总理今天来我家了,我感到非常荣幸'
words, postags, child_dict_list, roles_dict, format_parse_list = parse.parser_main(sentence)
print(words, len(words))
print(postags, len(postags))
print(child_dict_list, len(child_dict_list))
# print(roles_dict)
# print(format_parse_list, len(format_parse_list))
print(parse.get_verbs('缘尽至此？景甜张继科猝不及防的分手？景甜九字回应引网友热议'))