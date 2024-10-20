from app.initiate_app import create_app  # Import the create_app function from the right module

app = create_app()  

# Call the factory function to create the Flask app instance

if __name__ == '__main__':
    app.run(debug=True)
