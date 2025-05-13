from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID
def find_event_by_id(event_id):
    """
    Helper function to find an event by its ID
    
    Args:
        event_id (int): The ID of the event to find
        
    Returns:
        Event: The found event object or None if not found
    """
    for event in events:
        if event.id == event_id:
            return event
    return None

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    """
    Create a new event from JSON input
    
    Expects a JSON body with a 'title' field
    
    Returns:
        JSON: The created event data with status code 201
        or error message with status code 400 if validation fails
    """
    # Get JSON data from request
    data = request.get_json()
    
    # Validate input
    if not data or 'title' not in data:
        return jsonify({"error": "Missing required field: title"}), 400
    
    # Generate a new ID (simple approach for in-memory storage)
    new_id = max(event.id for event in events) + 1 if events else 1
    
    # Create new event
    new_event = Event(new_id, data['title'])
    events.append(new_event)
    
    # Return the created event with 201 Created status
    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    """
    Update the title of an existing event
    
    Args:
        event_id (int): The ID of the event to update
        
    Expects a JSON body with a 'title' field
    
    Returns:
        JSON: The updated event data with status code 200
        or error message with status code 404 if event not found
        or error message with status code 400 if validation fails
    """
    # Find the event
    event = find_event_by_id(event_id)
    
    # If event doesn't exist, return 404
    if not event:
        return jsonify({"error": f"Event with ID {event_id} not found"}), 404
    
    # Get JSON data from request
    data = request.get_json()
    
    # Validate input
    if not data or 'title' not in data:
        return jsonify({"error": "Missing required field: title"}), 400
    
    # Update the event
    event.title = data['title']
    
    # Return the updated event
    return jsonify(event.to_dict()), 200

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """
    Delete an event by ID
    
    Args:
        event_id (int): The ID of the event to delete
        
    Returns:
        No content with status code 204 if successful
        or error message with status code 404 if event not found
    """
    # Find the event
    event = find_event_by_id(event_id)
    
    # If event doesn't exist, return 404
    if not event:
        return jsonify({"error": f"Event with ID {event_id} not found"}), 404
    
    # Remove the event from the list
    events.remove(event)
    
    # Return success with no content (204)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)