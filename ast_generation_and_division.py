import os
import javalang
from anytree import AnyNode
from javalang.ast import Node
import pickle
import itertools
import json
import csv
import time
from multiprocessing import Pool
from functools import partial

nodetypedict = {'MethodDeclaration': 0, 'Modifier': 1, 'FormalParameter': 2, 'ReferenceType': 3, 'BasicType': 4,
     'LocalVariableDeclaration': 5, 'VariableDeclarator': 6, 'MemberReference': 7, 'ArraySelector': 8, 'Literal': 9,
     'BinaryOperation': 10, 'TernaryExpression': 11, 'IfStatement': 12, 'BlockStatement': 13, 'StatementExpression': 14,
     'Assignment': 15, 'MethodInvocation': 16, 'Cast': 17, 'ForStatement': 18, 'ForControl': 19,
     'VariableDeclaration': 20, 'TryStatement': 21, 'ClassCreator': 22, 'CatchClause': 23, 'CatchClauseParameter': 24,
     'ThrowStatement': 25, 'WhileStatement': 26, 'ArrayInitializer': 27, 'ReturnStatement': 28, 'Annotation': 29,
     'SwitchStatement': 30, 'SwitchStatementCase': 31, 'ArrayCreator': 32, 'This': 33, 'ConstructorDeclaration': 34,
     'TypeArgument': 35, 'EnhancedForControl': 36, 'SuperMethodInvocation': 37, 'SynchronizedStatement': 38,
     'DoStatement': 39, 'InnerClassCreator': 40, 'ExplicitConstructorInvocation': 41, 'BreakStatement': 42,
     'ClassReference': 43, 'SuperConstructorInvocation': 44, 'ElementValuePair': 45, 'AssertStatement': 46,
     'ElementArrayValue': 47, 'TypeParameter': 48, 'FieldDeclaration': 49, 'SuperMemberReference': 50,
     'ContinueStatement': 51, 'ClassDeclaration': 52, 'TryResource': 53, 'MethodReference': 54, 'LambdaExpression': 55,
     'InferredFormalParameter': 56}

tokenindex = {'SuperMemberReference': 0, 'InnerClassCreator': 1, 'OctalInteger': 2, 'ClassDeclaration': 3, 'ElementArrayValue': 4,
              'ExplicitConstructorInvocation': 5, 'FieldDeclaration': 6, 'ElementValuePair': 7, 'TypeParameter': 8, 'AssertStatement': 9,
              'SuperConstructorInvocation': 10, 'DoStatement': 11, 'SuperMethodInvocation': 12, 'SynchronizedStatement': 13, 'SwitchStatement': 14,
              'SwitchStatementCase': 15, 'ContinueStatement': 16, 'DecimalFloatingPoint': 17, 'HexInteger': 18, 'ConstructorDeclaration': 19,
              'Keyword': 20, 'ArrayInitializer': 21, 'TernaryExpression': 22, 'ClassReference': 23, 'BreakStatement': 24,
              'EnhancedForControl': 25, 'Annotation': 26, 'TypeArgument': 27, 'This': 28, 'ThrowStatement': 29,
              'ArraySelector': 30, 'ArrayCreator': 31, 'ForControl': 32, 'WhileStatement': 33, 'VariableDeclaration': 34,
              'ForStatement': 35, 'Boolean': 36, 'Cast': 37, 'CatchClause': 38, 'CatchClauseParameter': 39,
              'TryStatement': 40, 'Null': 41, 'ReturnStatement': 42, 'DecimalInteger': 43, 'IfStatement': 44,
              'BasicType': 45, 'Assignment': 46, 'BlockStatement': 47, 'ClassCreator': 48, 'String': 49,
              'FormalParameter': 50, 'BinaryOperation': 51, 'LocalVariableDeclaration': 52, 'Operator': 53, 'VariableDeclarator': 54,
              'Literal': 55, 'StatementExpression': 56, 'ReferenceType': 57, 'MethodInvocation': 58, 'MemberReference': 59,
              'MethodDeclaration': 60, 'Modifier': 61, 'Identifier': 62}


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def get_token(node):
    token = ''
    # print(isinstance(node, Node))
    # print(type(node))
    if isinstance(node, str):
        token = node
    elif isinstance(node, set):
        token = 'Modifier'
    elif isinstance(node, Node):
        token = node.__class__.__name__
    # print(node.__class__.__name__,str(node))
    # print(node.__class__.__name__, node)
    return token


def get_child(root):
    # print(root)
    if isinstance(root, Node):
        children = root.children
    elif isinstance(root, set):
        children = list(root)
    else:
        children = []

    def expand(nested_list):
        for item in nested_list:
            if isinstance(item, list):
                for sub_item in expand(item):
                    # print(sub_item)
                    yield sub_item
            elif item:
                # print(item)
                yield item

    return list(expand(children))


def createtree(root, node, nodelist, parent=None):
    id = len(nodelist)
    # print(id)
    token, children = get_token(node), get_child(node)
    if id == 0:
        root.token = token
        root.data = node
    else:
        newnode = AnyNode(id=id, token=token, data=node, parent=parent)
    nodelist.append(node)
    for child in children:
        if id == 0:
            createtree(root, child, nodelist, parent=root)
        else:
            createtree(root, child, nodelist, parent=newnode)


def getnodeandedge(node, tokentypedict, twotypes):
    for child in node.children:
        if len(child.children) == 0:
            try:
                child.token = tokentypedict[child.token]
            except KeyError:
                if child.token not in nodetypedict:
                    child.token = 'String'
        twotypes.append([node.token, child.token])
        getnodeandedge(child, tokentypedict, twotypes)


def traverse(node, typedict, triads, path=None):
    if path is None:
        path = []
    if len(node.children) == 0:
        try:
            node.token = typedict[node.token]
        except KeyError:
            if node.token != 'ReturnStatement':
                node.token = 'Null'
        path.append(node.token)
        if len(path) >= 3:
            triad = [path[-3], path[-2], path[-1]]
            triads.append(triad)
        yield path
        path.pop()
    else:
        path.append(node.token)
        if len(path) >= 3:
            triad = [path[-3], path[-2], path[-1]]
            triads.append(triad)
        for child in node.children:
            yield from traverse(child, typedict, triads, path)
        path.pop()


def fsstype(node, triads, tokenindex):
    children = []
    for child in node.children:
        children.append(child.token)
    for i in itertools.combinations(children, 2):
        if tokenindex[i[0]] <= tokenindex[i[1]]:
            triads.append([node.token, i[0], i[1]])
        else:
            triads.append([node.token, i[1], i[0]])
    for child in node.children:
        fsstype(child, triads, tokenindex)


def one_txt(path, dataset, n_gram):

    print(path)
    # 生成ast和token
    programfile = open(path, encoding='utf-8')
    programtext = programfile.read()
    programtokens = javalang.tokenizer.tokenize(programtext)
    parser = javalang.parse.Parser(programtokens)
    tree = parser.parse_member_declaration()

    programfile.close()

    file = open(path, "r", encoding='utf-8')
    tokens = list(javalang.tokenizer.tokenize(file.read()))
    # print("programtokens", list(tokens))
    file.close()

    # 生成树
    nodelist = []
    newtree = AnyNode(id=0, token=None, data=None)
    createtree(newtree, tree, nodelist)

    # 生成类型字典
    typedict = {}
    for token in tokens:
        token_type = str(type(token))[:-2].split(".")[-1]
        token_value = token.value
        if token_value not in typedict:
            typedict[token_value] = token_type
        else:
            if typedict[token_value] != token_type:
                print('!!!!!!!!')

    if n_gram == '2-gram':
        type2 = []
        getnodeandedge(newtree, typedict, type2)

        # 生成文本
        types = []
        for t in type2:
            triad = str(t[0] + '/' + t[1])
            types.append(triad)
        # name = path.split('/')[-1].split('.java')[0]
        # txtname = './' + dataset + '_2gram_txt/' + name + '.txt'
        # with open(txtname, 'w') as f:
        #     #f.write(str(types))
        #     for line in types:
        #         f.write(line + ',')
        return types

    elif n_gram == '3-gram':
        # 统计父子孙类型并规范叶子结点
        type1triads = []
        paths = traverse(newtree, typedict, type1triads)
        i = 0
        for p in paths:
            # print(p)
            i += 1

        # 统计父子子类型
        type2triads = []
        fsstype(newtree, type2triads, tokenindex)

        # 生成文本
        types = []
        for t in type1triads:
            triad = str('1' + t[0] + '/' + t[1] + '/' + t[2])
            types.append(triad)
        for t in type2triads:
            triad = str('2' + t[0] + '/' + t[1] + '/' + t[2])
            types.append(triad)
        # name = path.split('/')[-1].split('.java')[0]
        # txtname = './' + dataset + '_3gram_txt/' + name + '.txt'
        # print(types)
        # with open(txtname, 'w') as f:
        #     # f.write(str(types))
        #     for line in types:
        #         f.write(line + ',')
        return types


# 生成每个文件的类型文档
def main3(javalist, dataset, n_gram):
    for javafile in javalist:
        #print(javafile)
        one_txt(javafile, dataset, n_gram)


if __name__ == '__main__':
    # 从文件夹中读取所有Java文件
    javapath = '/home/data4T/wym/fsl/traids/dataset/id2sourcecode'
    #javapath = '/home/data4T/wym/fsl/markovchain/GCJ'
    javalist = []
    listdir(javapath, javalist)

    start1 = time.time()
    main3(javalist, 'BCB', '2-gram')
    end1 = time.time()
    t1 = end1 - start1
    print('2-gram get_txt time:')
    print(t1)

    # start2 = time.time()
    # main3(javalist, 'BCB', '3-gram')
    # end2 = time.time()
    # t2 = end2 - start2
    # print('3-gram get_txt time:')
    # print(t2)
