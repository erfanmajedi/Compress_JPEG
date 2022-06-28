class Node : 
    def __init__(self, prob, symbol, left = None, right = None) :
        # probability
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''
# calculate the probability
def Calc_Probability(data) :
    symbols = dict()
    for element in data :
        if symbols.get(element) == None :
            symbols[element] = 1 
        else :
            symbols[element] += 1
    return symbols

codes = dict()
# print codes of symbols by traveling huffman tree
def Calc_Codes(node, val = '') :
    curr_val = val + str(node.code)

    if (node.left) :
        Calc_Codes(node.left, curr_val)

    if(node.right) :
        Calc_Codes(node.right, curr_val)

    if(not node.left and not node.right) :
        codes[node.symbol] = curr_val
    return codes

# obtain the encoded output
def Out_Encode(data, coding) :
    encoding_output = []
    for c in data : 
        print(coding[c], end = '')
        encoding_output.append(coding[c])
    
    string = ''.join([str(item) for item in encoding_output])
    return string

# calculate the space difference between compressed and non compressed 
def total_gain(data, coding) :
    before_compression = len(data) * 8
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols :
        count = data.count(symbol)
        after_compression += count * len(coding[symbol])
    print("Space Before Compression in Bits :", before_compression)
    print("Space After Compression in Bits :", after_compression)

def huffman(data) : 
    symbol_with_probability = Calc_Probability(data)
    symbols =  symbol_with_probability.keys()
    probabilities = symbol_with_probability.values()
    print("symbols :", symbols)
    print("probabilities:", probabilities)

    nodes = []
    #  convertion of symbols and probabilities into huffman tree nodes
    for symbol in symbols :
        nodes.append(Node(symbol_with_probability.get(symbol), symbol))
    
    while len(nodes) > 1 :
        # sort based on probability
        nodes = sorted(nodes, key = lambda x: x.prob)
        right = nodes[0]
        left = nodes[1]
        left.code = 0
        right.code = 1

        newNode = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)

    huffman = Calc_Codes(nodes[0])
    print(huffman)
    total_gain(data, huffman)
    encoded_output = Out_Encode(data, huffman)
    print("\tEncoded Output:", encoded_output)
    return encoded_output, nodes[0]

inputData = input().split()
huffman(inputData)

