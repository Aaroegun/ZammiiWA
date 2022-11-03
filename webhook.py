from flask import Flask, request, Response
app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def return_response():
    print(request.json);

    return Response(status=200)

@app.route('/webhook', methods=['GET'])
def return_responses():
    args = request.args
    mode = args.get("hub.mode")
    token = args.get("hub.verify_token")
    challenege = args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == "Hitesh123":
            print("Success")
            return Response(status=200, challenege=challenege)
        else:
            print("fail to verify")
            return Response(status=403)


if __name__ == "__main__": app.run()