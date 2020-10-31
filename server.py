from flask import Flask
from flask import request, jsonify, abort, make_response
from flask_cors import CORS

try:
    import simplejson as json
except ImportError:
    import json
try:
    from http import HTTPStatus
except ImportError:
    import httplib as HTTPStatus

from kep import YAKE

import argparse

app = Flask(__name__)
CORS(app)

listOfDatasets = [  '110-PT-BN-KP', 
                    '500N-KPCrowd-v1.1', 
                    'cacic', 
                    'citeulike180', 
                    'fao30', 
                    'fao780', 
                    'Inspec', 
                    'kdd', 
                    'Krapivin2009', 
                    'Nguyen2007', 
                    'pak2018', 
                    'PubMed', 
                    'Schutz2008', 
                    'SemEval2010', 
                    'SemEval2017', 
                    'theses100', 
                    'wicc', 
                    'wiki20', 
                    'WikiNews', 
                    'www']

@app.route('/kep', methods=['POST'])
def handle_kep():

    try:
        assert request.json["text"] , "Invalid text"
        assert int(request.json["num_keyphrases"]) , "Invalid num_keyphrases"

        # Some algorithms need to know the path of the dataset in order to create some models
        dataset = request.args.get('dataset', '500N-KPCrowd-v1.1')
        text = request.json["text"]
        num_keyphrases = int(request.json["num_keyphrases"])

        yake_object = YAKE(num_keyphrases, args.datadir, dataset)
        phrases = yake_object.runSingleDoc(text)
        result  = [{"score":x[1] ,"phrase":x[0]} for x in phrases]

        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return jsonify(str(e)), HTTPStatus.BAD_REQUEST

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-datadir', dest='datadir', help='', default='/opt/shared')
    parser.add_argument('-dataset', dest='dataset', help='', default='500N-KPCrowd-v1.1')
    parser.add_argument('-port', dest='port', help='', default=5009)
    parser.add_argument('-host', dest='host', help='', default='0.0.0.0')
    parser.add_argument('-debug', dest='debug', help='', default=False)    
    args = parser.parse_args()
    app.run(host=args.host, port=int(args.port), debug=args.debug)
