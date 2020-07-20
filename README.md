# Simple blockchain app using flask

This a simple app to showcase how blockchain basically works.

## Testing
Fork and clone the project first. Then in project directory.    

### For single node

    python3 -m venv env 
    source env/bin/activate
    pip3 install -r requirements.txt
    export FLASK_APP=app.py
    flask run
    
### For multiple nodes
Open multiple shell windows and run this command with different ports.
Example:
    
In one shell:
    
    flask run -p 5000
    
In another shell:

    flask run -p 5001
    
## Credits
This repo was not possible with support. From https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
