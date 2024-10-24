import requests

def predict_water_level(forward_days=5):
    # Define the API endpoint
    url = "https://kay168-water-level-forecast.hf.space/predict"
    
    # Define the input data
    input_data = {"forward": forward_days}
    
    try:
        # Make a GET request to the API
        response = requests.get(url, json=input_data)
        
        # Check the response status code
        if response.status_code == 200:
            # Return the response data
            return response.json()
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {e}"
