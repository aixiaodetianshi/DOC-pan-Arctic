from graphviz import Digraph

# 创建有向图  # English: Create a directed graph
dot = Digraph()

# 添加节点和边  # English: Add nodes and edges
dot.node('A', '开始')
dot.node('B', '步骤1')
dot.node('C', '步骤2')
dot.node('D', '结束')

dot.edges(['AB', 'BC', 'CD'])

# 渲染流程图  # English: Rendering flowchart
dot.view()

