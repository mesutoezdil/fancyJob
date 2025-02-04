from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Simulated database (for demonstration purposes)
users_db = {
    1: {"name": "John", "email": "john@example.com"},
    2: {"name": "Jane", "email": "jane@example.com"}
}

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# Get a user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users_db.get(user_id)
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"error": "Missing required fields (name, email)"}), 400
    
    new_id = max(users_db.keys()) + 1  # New user ID (for simplicity)
    new_user = {
        "name": data['name'],
        "email": data['email']
    }
    users_db[new_id] = new_user
    return jsonify({"message": "User created successfully", "user": new_user}), 201

# Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = users_db.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    
    return jsonify({"message": "User updated successfully", "user": user}), 200

# Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = users_db.pop(user_id, None)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully"}), 200

# Calculate the square of a number
@app.route('/square', methods=['POST'])
def square_number():
    data = request.get_json()
    try:
        number = data['number']
        result = number ** 2
        return jsonify({'result': result}), 200
    except KeyError:
        return jsonify({'error': 'No "number" key in request body'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add two numbers
@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    try:
        number1 = data['number1']
        number2 = data['number2']
        result = number1 + number2
        return jsonify({'result': result}), 200
    except KeyError:
        return jsonify({'error': 'Missing "number1" or "number2"'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Calculate the factorial of a number
@app.route('/factorial', methods=['POST'])
def calculate_factorial():
    data = request.get_json()
    try:
        number = data['number']
        if number < 0:
            raise ValueError("Factorial does not exist for negative numbers")
        result = 1
        for i in range(1, number + 1):
            result *= i
        return jsonify({'result': result}), 200
    except KeyError:
        return jsonify({'error': 'No "number" key in request body'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

# Handle other errors
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
