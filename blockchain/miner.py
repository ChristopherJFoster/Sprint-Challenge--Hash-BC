import hashlib
import requests  # pylint: disable=F0401

import sys

from uuid import uuid4

import time

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")

    last_hash = hashlib.sha256(f'{last_proof}'.encode()).hexdigest()

    proof = None
    proof0 = 0
    proof1 = 3000000
    proof2 = 6000000
    proof3 = 9000000
    proof4 = 12000000
    proof5 = 15000000
    proof6 = 18000000
    proof7 = 21000000
    proof8 = 24000000
    proof9 = 27000000

    start = time.time()
    counter = 1
    alert = False

    while proof == None and alert == False and valid_proof(last_hash, proof0) is False and valid_proof(last_hash, proof1) is False and valid_proof(last_hash, proof2) is False and valid_proof(last_hash, proof3) is False and valid_proof(last_hash, proof4) is False and valid_proof(last_hash, proof5) is False and valid_proof(last_hash, proof6) is False and valid_proof(last_hash, proof7) is False and valid_proof(last_hash, proof8) is False and valid_proof(last_hash, proof9) is False:
        proof0 += 1
        proof1 += 1
        proof2 += 1
        proof3 += 1
        proof4 += 1
        proof5 += 1
        proof6 += 1
        proof7 += 1
        proof8 += 1
        proof9 += 1

        if (time.time() - start) > (counter * 5):
            counter += 1
            r = requests.get(url=node + "/last_proof")
            data = r.json()
            current_last_proof = data.get('proof')
            if current_last_proof == last_proof:
                print('same!')
            else:
                print('different!')
                start = time.time()
                counter = 1
                last_proof = current_last_proof
                last_hash = hashlib.sha256(
                    f'{current_last_proof}'.encode()).hexdigest()
                proof = None
                proof0 = 0
                proof1 = 3000000
                proof2 = 6000000
                proof3 = 9000000
                proof4 = 12000000
                proof5 = 15000000
                proof6 = 18000000
                proof7 = 21000000
                proof8 = 24000000
                proof9 = 27000000
        if counter == 14:
            print('ALERT! proof9: ', proof9)
            proof9 = 35000000
            alert = True

    if valid_proof(last_hash, proof0) is True:
        print('proof0')
        proof = proof0
    elif valid_proof(last_hash, proof1) is True:
        print('proof1')
        proof = proof1
    elif valid_proof(last_hash, proof2) is True:
        print('proof2')
        proof = proof2
    elif valid_proof(last_hash, proof3) is True:
        print('proof3')
        proof = proof3
    elif valid_proof(last_hash, proof4) is True:
        print('proof4')
        proof = proof4
    elif valid_proof(last_hash, proof5) is True:
        print('proof5')
        proof = proof5
    elif valid_proof(last_hash, proof6) is True:
        print('proof6')
        proof = proof6
    elif valid_proof(last_hash, proof7) is True:
        print('proof7')
        proof = proof7
    elif valid_proof(last_hash, proof8) is True:
        print('proof8')
        proof = proof8
    elif valid_proof(last_hash, proof9) is True:
        print('proof9')
        proof = proof9

    while alert == True and proof == None and valid_proof(last_hash, proof) is False:
        proof9 += 1

    while proof == None and valid_proof(last_hash, proof) is False:
        proof9 += 1

    if proof == None:
        proof = proof9

    end = time.time()
    print('Proof found: ' + str(proof) + ' in ' +
          str(round((end - start), 2)) + ' seconds')
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """

    guess = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == last_hash[-6:]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        print('last_proof: ', data.get('proof'))
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
