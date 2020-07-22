from blockchain import Blockchain
import json

from uuid import uuid4
from flask import Flask, request, Response

# Instantiate our Node
app = Flask(__name__)

# Generate a unique address for this Node
node_indentifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algo to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof ...
    # The sender is "0" to signify that this node has mined a new coin
    blockchain.new_transaction(
        sender="0",
        recipient=node_indentifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return Response(json.dumps(response), content_type='application/json; charset=utf-8'), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POSTed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return Response(json.dumps(response), content_type='application/json; charset=utf-8'), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return Response(json.dumps(response), content_type='application/json; charset=utf-8'), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    
    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return Response(json.dumps(response), content_type='application/json; charset=utf-8'), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conficts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain,
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'new_chain': blockchain.chain,
        }
    return Response(json.dumps(response), content_type='application/json; charset=utf-8'), 200