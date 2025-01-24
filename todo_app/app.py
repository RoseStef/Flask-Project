from Website import create_app

app = create_app()#Function runs the application via gunicorn, and build it from there not via python app.py script, which on the other hand is done from line 5 locally. 

if __name__=="__main__":
    app = create_app()
    app.run(debug=True, port=8000) 