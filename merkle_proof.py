from utils import *
import math
from node import Node


def merkle_proof(tx, merkle_tree):
    """Given a tx and a Merkle tree object, retrieve its list of tx's and
    parse through it to arrive at the minimum amount of information required
    to arrive at the correct block header. This does not include the tx
    itself.

    Return this data as a list; remember that order matters!
    """
    proof_list = []
    current_node = merkle_tree._root
    tx_index = merkle_tree.leaves.index(tx)
    upper_bound = len(merkle_tree.leaves)
    lower_bound = 0
    while upper_bound - lower_bound > 1:
        mid = (upper_bound + lower_bound) // 2
        if tx_index < mid:
            proof_list.append(Node('r', current_node._right.data if type(
                current_node._right) != str else current_node._right))
            current_node = current_node._left
            upper_bound = mid
        else:
            proof_list.append(Node('l', current_node._left.data if type(
                current_node._left) != str else current_node._left))
            current_node = current_node._right
            lower_bound = mid
    return proof_list





def verify_proof(tx, merkle_proof):
    """Given a Merkle proof - constructed via `merkle_proof(...)` - verify
    that the correct block header can be retrieved by properly hashing the tx
    along with every other piece of data in the proof in the correct order
    """
    # merkle_proof = ([node.tx for node in merkle_proof])[::-1]
    # return concat_and_hash_list(merkle_proof)
    tx_list = [tx] + merkle_proof[::-1]
    while len(tx_list) > 1:
        if tx_list[1].direction == 'r':
            tx_list.insert(0, hash_data(tx_list.pop(0) + tx_list.pop(0).tx))
        else:
            tx_list.insert(0, hash_data(tx_list.pop(1).tx + tx_list.pop(0)))
    return tx_list[0]
    
