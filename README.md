Photo Frame Server:

This is a flask server used to upload and delete photos from a SQL database being saved on a Raspberry Pi which is then used to display a picture on a monitor.

So far the server has a POST photo, GET random and a DELETE delete route to allow for manipulation of the database. 

the POST photo, allows the user to add a photo to the database to be shown.
the GET random, pulls a random photo from the data base to display.
the DELETE delete, removes the photo from the database but leaves a trace for updating multiple users.

Apple shortcuts have been made for quick access to each of the routes on the server while it is running. This also allows for the 
photos saved on a users computer to be used and uploaded.
