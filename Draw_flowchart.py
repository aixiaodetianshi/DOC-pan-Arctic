from graphviz import Digraph

# 创建有向图
dot = Digraph()

# 添加节点和边
dot.node('A', '开始')
dot.node('B', '步骤1')
dot.node('C', '步骤2')
dot.node('D', '结束')

dot.edges(['AB', 'BC', 'CD'])

# 渲染流程图
dot.view()

