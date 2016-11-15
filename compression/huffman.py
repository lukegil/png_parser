

class HuffByte(object):
    """ a data object representing a byte, its encoding, and its frequency
        in a given document
    """
    def __init__(self, value=bytes(), encoded_value=int(), frequency=float()):
        """
            value
                @type - bytes
                @param - the byte found in a source document

            encoded_value
                @type - int
                @param - the integer given as the byte value by the huffman
                         tree.

            frequency
                @type - float
                @param - (# times this byte appears) / (total bytes in doc)
        """
        self.value = value,
        self.encoded_value = encoded_value
        self.frequency = frequency


class Node(object):
    def __init__(self):
        self._left = None
        self._right = None
        self._value = HuffByte(None, 0, 0)

    @property
    def left(self):
        """ the left branch of Node """
        return self._left

    @left.setter
    def left(self, node):
        """ set the left branch of Node

            @type - Node
            @param - the node the left edge should reference
        """
        self._left = node

    @property
    def right(self):
        """ the right branch of Node """
        return self._right

    @right.setter
    def right(self, node):
        """ set the right branch of Node

            @type - Node
            @param - the node the right edge should reference
        """
        self._right = node

    @property
    def value(self):
        """ the value of a Node, defaults to None """
        return self._value

    @value.setter
    def value(self, val):
        """ set the value of Node

            @type - any
            @param - value of the Node
        """
        self._value = val


class HuffmanTree(object):
    """ A Huffman Tree, comprised of (i) a mapping of byte-values to encodings
        and (ii) a pointer to a tree's root Node. Left turns are 1, right turns are 0

        The two attributes either return themselves, try to build themselves
        out of the other attribute, or return None
    """
    def __init__(self):
        """
        _mapping
            @type - dic
            @param - Keys are a byte value (aka Huffbyte.value).
                     Values are HuffBytes

        _tree
            @type - Node
            @param - the root node to a Huffman tree.
        """
        self._mapping = {}
        self._tree = Node()

    @property
    def mapping(self):

        # If we have it, return the mapping
        if (self._mapping):
            return self._mapping
        # Otherwise, try to build it out of the tree, and return it
        elif (self._tree):
            self.mapping = self._build_mapping()
            return self.mapping
        # If we can't do anything, just return None
        else:
            return None

    @mapping.setter
    def mapping(self, map_dict):
        """ sets value of `mapping` attribute

            @type - dic
            @param - {HuffByte.value : HuffByte}
        """
        self._mapping = map_dict

    @property
    def tree(self):
        # If we have a tree, return it
        if (self._tree):
            r = self._tree
        # If we don't try to build it out of the mapping and return it
        elif (self._mapping):
            self.tree = self._build_tree()
            r = self.tree
        # finally, just return None
        else:
            r = None

        return r

    @tree.setter
    def tree(self, node):
        self._tree = node

    def _build_mapping(self):
        """ From a Huffman tree, recursively build a mapping of byte values to HuffBytes """
        root_node = self.tree
        mapping = {}
        self._get_leaves(root_node, 1, mapping)
        return mapping

    def _get_leaves(self, cur_node, path, mapping):
        """ recursively walk down a tree and get leaves

            cur_node
                @type - Node
                @param - a Node. If value is None, then is not a leaf

            path
                @type - int
                @param - the current integer representation of the value based on
                         the huffman tree. All begin with 1

            mapping
                @type - dic
                @param - the output dict of {HuffByte.value : HuffByte}
        """

        # we found a leaf
        if (cur_node and cur_node.value):
            cur_node.encoded_value = path
            mapping[cur_node.value] = cur_node

        # no leaf found, try to take the left and right branches
        elif (cur_node):
            l_np = (path << 1) ^ 1 #append 1
            r_np = (path << 1) #append 0

            self._get_leaves(cur_node.left, l_np, mapping)
            self._get_leaves(cur_node.right, r_np, mapping)

    def _build_tree(self):
        """ From _mapping, build a Huffman Tree of Nodes() """
        root = Node()
        mapping = self.mapping
        for key in mapping:
            v = mapping[key]
            self._add_leaves(root, v.encoded_value.bit_length() - 1, v)

        return root

    def _add_leaves(self, prev_node, cur_shift, leaf_val):
        """ Recursively build a tree, based on encoded values of a HuffByte

            prev_node
                @type - Node
                @param - the node that references the one we walked to

            cur_shift
                @type - int
                @param - the nth bit of leaf_val.encoded_value

            leaf_val
                @type - HuffByte
                @param - the value we're trying to add to a leaf
        """


        # Ensure that either the right or left node exists (depending on value
        # of direction). If not, build add it
        direction = (leaf_val.encoded_value >> cur_shift) & 1
        cur_shift -= 1

        if (direction == 1 and prev_node.left is None):
            new_node = Node()
            prev_node.left = new_node

        elif (direction == 0 and prev_node.right is None):
            new_node = Node()
            prev_node.right = new_node

        # BASE CASE - we've reached the bottom of the tree, add leaf_val and return
        if (cur_shift == 0):
            new_node.value = leaf_val
            return

        # Otherwise, take the given branch and recall the function
        n = prev_node.left if direction else prev_node.right
        self._add_leaves(n, cur_shift, leaf_val)


class EncodeStream(object):
    def __init__(self):
        self._raw_stream = bytearray()
        self._encoded_stream = bytearray()
        self._huffman_tree = HuffmanTree()

    @property
    def raw_stream(self):
        """ the input to be encoded """
        return self._raw_stream

    @raw_stream.setter
    def raw_stream(self, stream):
        """ set the input stream

            @type - bytearray
            @param - the bytearray to be encoded
        """
        self._raw_stream = stream

    @property
    def encoded_stream(self):
        """ the encoded output """
        return self._encoded_stream

    @raw_stream.setter
    def encoded_stream(self, stream):
        """ set the input stream

            @type - bytearray
            @param - the bytearray that was encoded
        """
        self._encoded_stream = stream

    def encode(self, sample_size=1.00):
        huffbytes = build_huffByte_freqs(self.raw_stream, sample_size)
        node_list = huffBytes_to_Nodes(freqs)
        node_list = sort_NodeList(node_list)
        self._huffman_tree = build_huffman_tree(node_list)
        self.encoded_stream = self._pack_input(self.raw_stream, self._huffman_tree.mapping)


    def _pack_input(stream, mapping):
        output = bytearray()
        bspace = 7
        in_byte = 0
        out_byte = 1

        while stream or cache:

            if (not in_byte and mapping.get(stream[0], None) is None):
                output.append(stream[0])
                stream = stream[1:]

            elif (not in_byte):
                in_byte = mapping.get(stream[0], None)

            # If the entire number excluding the first
            # bit  will fit in byte, add it
            l = in_byte.value.bit_length() - 1
            if (l <= bspace):
                out_byte = append_to_int(out_byte, in_byte)
                bspace -= l
                in_byte = 0
                cur_stream = cur_stream[1:]

            else:
                # Get left n bits, add to out_byte, and push
                # to output
                shift = in_byte.bit_length() - bspace
                b = in_byte >> shift
                out_byte = append_to_int(out_byte, b)
                output.append(out_byte)

                # Take the untouched bits, and prepend a 1
                mask = (1 << shift) - 1
                in_byte &= mask
                in_byte |= (1 << shift)

                # Next loop will start a new byte
                out_byte = 1
                bspace = 7

        return output

    def decode(self):
        pass



def build_huffByte_freqs(byte_stream, sample_size=1.00):
    """ Returns list of HuffBytes with frequencies set

        byte_stream
            @type - bytearray
            @param - the raw data

        sample_size
            @type - float
            @param - what percent of the data to review for frequencies
    """
    up_to = len(byte_stream) * sample_perc
    byte_stream = byte_stream[:int(up_to)]
    freq_tbl = {}
    max_freq = 0
    for byte in byte_stream:
        try:
            freq_tbl[byte].frequency += 1/up_to

        except KeyError:
            b = HuffByte(value = byte, frequency = 1/up_to)
            freq_tbl[byte] = b

    return values(freq_tbl)

def huffBytes_to_Nodes(hb_list):
    return [hb_to_node(hb) for hb in hb_list]

def hb_to_node(hb):
    new_node = Node()
    new_node.value = hb
    return new_node

def sort_NodeList(node_list, pivot=None):
    """ Sort a set of Nodes with HuffByte values into desc by frequency using quicksort """
    if (len(node_list) <= 1):
        return node_list

    if (pivot is None):
        pivot = node_list[len(node_list)/2].value.frequency

    smaller = []
    larger = []
    for i in range(pivot):
        n = hb_list[pivot]
        if (n.value.frequency < p):
            smaller.append(n)
        else:
            larger.append(n)

    return sort_HuffBytes([larger]) + sort_HuffBytes([smaller])

def insert_to_NodeList(node, node_list):
    """ Insert a new Node into huff_tbl sorted by probability DESC

        node - @type - tuple
             - @param - (Node, probability)

        node_list - @type - list
                 - @param - list of `tupe`s

        Insert into huff_tbl using binary-search insert, since
        insertion is being done asyncronously. Ordered desc to
        optimize for pop()s
    """
    found = False
    lwr = 0
    upr = len(node_list) - 1
    while not found:
        mid = (upr + lwr) // 2
        freq = node.frequency

        # empty table
        if (not node_list):
            found = True
            i_at = 0

        # Found midpoint
        elif ((upr - lwr) <= 1 and node_list[lwr][1] > freq > node_list[upr][1]):
            found = True
            i_at = upr

        # `prob` smaller than any in tbl
        elif (node_list[upr][1] >= freq):
            found = True
            i_at = upr + 1

        # `prob` larger than any in tbl
        elif (freq >= node_list[lwr][1]):
            found = True
            i_at = lwr

        # `prob` is midpoint
        elif (freq == node_list[mid][1]):
            found = True
            i_at = mid

        # prob is between lower and mid
        elif (node_list[lwr][1] > freq > node_list[mid][1]):
            upr = mid

        #prob is between mid and upper
        elif (node_list[mid][1] > freq > node_list[upr][1]):
            lwr = mid

    node_list.insert(i_at, node)
    return node_list

def build_huffman_tree(node_list):
    """ Returns a HuffmanTree object

        @type - {}
        @param - the bytestream to
        """
    while (len(node_list) > 1):
        n1 = node_list.pop()
        n2 = node_list.pop()

        new_node = Node()
        new_node.value.frequency = n1.frequency + n2.frequency
        node_list = insert_to_NodeList(new_node, node_list)

    HT = HuffmanTree()
    HT.tree = node_list[0]
    return HT

def append_to_int(int1, int2):
    """ bitwise append int2 to int1 and return
        NB: int2 has preceding 1 that should be stripped
    """
    l = int2.bit_length() - 1
    int1 <<= l

    int2 = int2 ^ (1 << l)
    int1 |= int2

    return int1
