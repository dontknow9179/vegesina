from pyltp import Segmentor,Postagger,NamedEntityRecognizer,SentenceSplitter,Parser,SementicRoleLabeller
import os
# import sys
# sys.path.append('../vegeserver/')
# import config as config

LTP_DATA_DIR = '../EventTriplesExtraction/ltp_data_v3.4.0'
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')# 词性标注模型路径，模型名称为`pos.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。


sents = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')  # 分句
print('\n'.join(sents))

segmentor=Segmentor() # 初始化实例
segmentor.load(cws_model_path)  # 加载模型
words=segmentor.segment('元芳你怎么看') # 分词结果
print(type(words))
print('\t'.join(words))
 
postagger = Postagger()
postagger.load(pos_model_path)
postags = postagger.postag(words)  # 词性标注
print('\t'.join(postags))

recognizer = NamedEntityRecognizer()
recognizer.load(ner_model_path)
netags = recognizer.recognize(words, postags)  # 命名实体识别
print('\t'.join(netags))

parser = Parser()
parser.load(par_model_path)
arcs = parser.parse(words, postags)  # 句法分析
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
rely_id = [arc.head for arc in arcs]    # 提取依存父节点id
relation = [arc.relation for arc in arcs]   # 提取依存关系
heads = ['Root' if id == 0 else words[id-1] for id in rely_id]  # 匹配依存父节点词语

for i in range(len(words)):
    print(relation[i] + '(' + words[i] + ', ' + heads[i] + ')')

labeller = SementicRoleLabeller()
labeller.load(srl_model_path)
roles = labeller.label(words, postags, arcs)  # 语义角色标注

for role in roles:
    print(role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))


labeller.release()
recognizer.release()  # 释放模型
segmentor.release()
postagger.release()
parser.release() 
