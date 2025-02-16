from flask import Flask, request
import requests
import re

app = Flask(__name__)

@app.route('/')
def index():
    # Get the 'javascript' query parameter from the URL
    js_param = request.args.get('javascript')
    if not js_param:
        return "Error: No 'javascript' parameter provided."

    # Use regex to extract all package names enclosed in parentheses.
    # For example, "(discord.js) (keyv)" will yield ["discord.js", "keyv"].
    packages = re.findall(r'\((.*?)\)', js_param)
    if not packages:
        return "Error: No packages found in the 'javascript' parameter."

    result = ""
    for package in packages:
        npm_url = f"https://www.npmjs.com/package/{package}"
        try:
            response = requests.get(npm_url)
            if response.status_code != 200:
                package_content = f"Error: Unable to retrieve package info (HTTP {response.status_code})."
            else:
                package_content = response.text
        except Exception as e:
            package_content = f"Error: {str(e)}"
        
        # Append the header and content for each package.
        result += f"Start of {package}\n{package_content}\n\n"

    return result

if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True)
