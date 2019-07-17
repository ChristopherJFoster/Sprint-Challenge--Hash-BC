#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    # put weights into hash table: key = weight, value = index
    for index in range(len(weights)):
        hash_table_insert(ht, weights[index], index)

    # check each weight in weights to see if there is another weight in the hash table that together equals the limit
    for index in range(len(weights)):
        if hash_table_retrieve(ht, limit - weights[index]) != None:
            if index > hash_table_retrieve(ht, limit - weights[index]):
                return (index, hash_table_retrieve(ht, limit - weights[index]))
            else:
                return (hash_table_retrieve(ht, limit - weights[index]), index)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
