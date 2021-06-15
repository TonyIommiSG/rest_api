import os
from flask import Flask, request, jsonify,render_template,Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_migrate import Migrate


app = Flask(__name__)

###################################################
################ CONFIGURATIONS ###################
##################################################

#for simplicity I have put the configs in the same file
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
basedir = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] deprecated due to heroku not updating their database url and not allowing me to change it either.
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)

###################################################
################ MODELS ###########################
##################################################


class Room(db.Model):
    __tablename__= 'Rooms'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    number = db.Column(db.Integer)
    occupant = db.Column(db.String(16))

    def __init__(self,name,number,occupant):
        self.name=name
        self.number=number
        self.occupant=occupant

    def json(self):
        return {
            'id':self.id,
            'name': self.name,
            'number':self.number,
            'occupant':self.occupant}

    def __str__(self):
        return f"{self.name} {self.number}"

###################################################
################ RESOURCES ########################
##################################################

class RoomResource(Resource):
    def get(self,name,number,occupant):

        room = Room.query.filter_by(name=name).first()

        if room:
            return room.json()
        else:
            # If you request a room not yet in the database
            return {'name':'not found'}, 404

    def post(self,name,number,occupant):
        """
        Create room with inputs: name(str), number(int), and occupant(str).
        Id's are created automatically and are the primary key.
        """
        room = Room(name=name,number=number,occupant=occupant)
        db.session.add(room)
        db.session.commit()

        return room.json()

    def put(self,name,number,occupant):

        room = Room.query.filter_by(name=name,number=number).first()

        if room:
            room.occupant = occupant
            db.session.commit()
            return room.json()
        else:
            # If you request a room not yet in the database
            return {'name':'not found'}, 404

    def delete(self,name,number,occupant):
        """
        Delete a room by inputting the name of the room.
        """
        room = Room.query.filter_by(name=name).first()
        db.session.delete(room)
        db.session.commit()

        return {'note':'delete successful'}




class AllRooms(Resource):

    def get(self):
        # return list of all rooms
        rooms = Room.query.all()

        # return json of rooms
        return [room.json() for room in rooms]


api.add_resource(RoomResource, '/room/<string:name>-<int:number>-<string:occupant>')
api.add_resource(AllRooms,'/rooms')

###################################################
################ Views ############################
##################################################

core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view.
    '''
    return render_template('index.html')

###################################################
################ Blueprint Configs ################
##################################################
app.register_blueprint(core)

if __name__ == '__main__':
    app.run(debug=True)
