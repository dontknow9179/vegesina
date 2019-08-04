from triple_extract.triple_extract import extractor

segmentor = extractor.parser.segmentor
postagger = extractor.parser.postagger
ltp_parser = extractor.parser.parser

def get_ltp_sub_entity(word_list, arcs):
    subs = []
    for i, arc in enumerate(arcs):
        if arc.relation == "SBV":  # subject verb
            subs.append(word_list[i])
    return subs


def get_ltp_obj_entity(word_list, arcs):
    objs = []
    for i, arc in enumerate(arcs):
        if arc.relation == "VOB":  # object verb
            objs.append(word_list[i])
    return objs


def get_ltp_predicate_entity(word_list, arcs):
    predicates = []
    for i, arc in enumerate(arcs):
        if arc.relation == "HED":
            predicates.append(word_list[i])
    return predicates


def get_ltp_entity_weight_dict(prep_article, entity_type, sentence_type='original', sentence_count=4):
    """
    对每篇文章title和中心句子提取 subject/object/predicate, 并对对应的类型计算每个词的权重
    :param prep_article: PreprocessArticle类的实例
    :param entity_type: 提取词的类型，取值为 sub/obj/predicate, 分别代表 subject, object, predicate
    :param sentence_type: 待提取的句子的排序方法，取值为 original/score, 分别代表 文章原始句子顺序，文章句子评分排序
    :param sentence_count: 中心句的个数，默认为4，如果为0，这只对title进行提取
    :return: subject/object/predicate的词-权重字典
    """
    entities = []
    # 文章title
    words = segmentor.segment(prep_article.title)
    word_list = list(words)
    postags = postagger.postag(words)
    arcs = ltp_parser.parse(words, postags)
    if entity_type == 'sub':
        entities.append(get_ltp_sub_entity(word_list, arcs))
    if entity_type == 'obj':
        entities.append(get_ltp_obj_entity(word_list, arcs))
    if entity_type == 'predicate':
        entities.append(get_ltp_predicate_entity(word_list, arcs))
    
    if sentence_count > 0:
        # 文章前n个句子
        if sentence_type == 'original':
            for i, sentence in enumerate(prep_article.sentences):
                if i < sentence_count:
                    words = segmentor.segment(sentence.text)
                    word_list = list(words)
                    postags = postagger.postag(words)
                    arcs = ltp_parser.parse(words, postags)
                    if entity_type == 'sub':
                        entities.append(get_ltp_sub_entity(word_list, arcs))
                    if entity_type == 'obj':
                        entities.append(get_ltp_obj_entity(word_list, arcs))
                    if entity_type == 'predicate':
                        entities.append(get_ltp_predicate_entity(word_list, arcs))
        # 文章得分降序前n个句子
        if sentence_type == 'score':
            for i, idx in enumerate(prep_article.descend_sentence_index):
                if i < sentence_count:
                    words = segmentor.segment(prep_article.sentences[idx].text)
                    word_list = list(words)
                    postags = postagger.postag(words)
                    arcs = ltp_parser.parse(words, postags)
                    if entity_type == 'sub':
                        entities.append(get_ltp_sub_entity(word_list, arcs))
                    if entity_type == 'obj':
                        entities.append(get_ltp_obj_entity(word_list, arcs))
                    if entity_type == 'predicate':
                        entities.append(get_ltp_predicate_entity(word_list, arcs))
    entity_weight_dict = calculate_weight(entities)
    return entity_weight_dict


def get_ltp_spo_weight_dict(prep_article, sentence_type='original', sentence_count=4):
    """
    对每篇文章title和中心句子提取subject, object, predicate, 并对subject, object, predicate计算每个词的权重
    :param prep_article: PreprocessArticle类的实例
    :param sentence_type: 待提取的句子的排序方法，取值为 original/score, 分别代表 文章原始句子顺序，文章句子评分排序
    :param sentence_count: 中心句的个数，默认为4，如果为0，这只对title进行提取
    :return: subject, object, predicate的词-权重字典
    """
    subs = []
    objs = []
    predicates = []
    # 文章title
    words = segmentor.segment(prep_article.title)
    word_list = list(words)
    postags = postagger.postag(words)
    arcs = ltp_parser.parse(words, postags)
    subs.append(get_ltp_sub_entity(word_list, arcs))
    objs.append(get_ltp_obj_entity(word_list, arcs))
    predicates.append(get_ltp_predicate_entity(word_list, arcs))
    # 文章句子
    if sentence_count > 0:
        # 文章前n个句子
        if sentence_type == 'original':
            for i, sentence in enumerate(prep_article.sentences):
                if i < sentence_count:
                    words = segmentor.segment(sentence.text)
                    word_list = list(words)
                    postags = postagger.postag(words)
                    arcs = ltp_parser.parse(words, postags)
                    subs.append(get_ltp_sub_entity(word_list, arcs))
                    objs.append(get_ltp_obj_entity(word_list, arcs))
                    predicates.append(get_ltp_predicate_entity(word_list, arcs))
        # 文章得分降序前n个句子
        if sentence_type == 'score':
            for i, idx in enumerate(prep_article.descend_sentence_index):
                if i < sentence_count:
                    words = segmentor.segment(prep_article.sentences[idx].text)
                    word_list = list(words)
                    postags = postagger.postag(words)
                    arcs = ltp_parser.parse(words, postags)
                    subs.append(get_ltp_sub_entity(word_list, arcs))
                    objs.append(get_ltp_obj_entity(word_list, arcs))
                    predicates.append(get_ltp_predicate_entity(word_list, arcs))

    sub_weight_dict = calculate_weight(subs)
    obj_weight_dict = calculate_weight(objs)
    predicate_weight_dict = calculate_weight(predicates)
    return sub_weight_dict, obj_weight_dict, predicate_weight_dict
