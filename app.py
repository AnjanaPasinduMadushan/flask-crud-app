from flask import Flask, request, render_template

import boto3

import dynamodb_handler as dynamodb

app = Flask(__name__)

@app.route('/')#decorator for home page
def root_route():
    # dynamodb.create_table_movie()
    # return 'Table Created'
    return render_template("index.html")

@app.route('/movie', methods=['POST'])

def add_movie():
    data = request.form.to_dict()
    response = dynamodb.add_item_to_movie_table(int(data['id']), data['title'], data['director'])
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
        }

    return {  
        'msg': 'Some error occcured',
        'response': response
    }
   
@app.route('/movie/<int:id>', methods=['GET'])
def get_movie(id):
    response = dynamodb.get_item_from_movie_table(id)
    
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        
        if ('Item' in response):
            return { 'Item': response['Item'] }

        return { 'msg' : 'Item not found!' }

    return {
        'msg': 'Some error occured',
        'response': response
    }

    
    
#define port and host
if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')