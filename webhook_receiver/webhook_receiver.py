from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the JSON data from the POST request
    data = request.json

    # Print the received data
    print("Received POST request with the following data:")
    print(data)

    # Return a response
    return "Received", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
