from thinkdb import app,socketio
from thinkdb import views
if __name__ == '__main__':
    #app.run(debug = True)
    socketio.run(app,debug = True,port=5001)