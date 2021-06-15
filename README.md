# rest_api
Room Rest Api for Technical Challenge 1

repo location:
  https://github.com/TonyIommiSG/rest_api

url for site:
  https://rooms-rest-api.herokuapp.com/

Explanation of Project:

  I decided to use Python and the Flask framework as this is what I am most familiar with
  and recently finished my own project with it. Flask is a micro-framework and
  simple to use, therefore I figured it would be perfect for writing this API.

  For prototyping and making calls besides GET (POST,PUT,DELETE), I used postman.

  With this API, you can create a room, with an id (created automatically),
  name, number, and occupant. Data is returned in JSON format.

  In order to make a call you simply type the url above and add:

      /room/<string:name>-<int:number>-<string:occupant>

  To update a room's occupant field, make a PUT call with the desired new occupant
  name.

  To delete a room type the url for the specific room following the format above.

  To see a list of all rooms currently stored use this url:

    https://rooms-rest-api.herokuapp.com/rooms

  The data is persisted using PostgreSQL. PostgreSQL is what is provided by Heroku
  for ease of use.
