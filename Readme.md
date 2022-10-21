  ## Introduction
  The API project aids in developing a parking management system. With is broken down into an android app and admin web dashboard


  ## Running the application
    /*
    ## House keeping

    1. set the application running env in windows by
    **py -m venv env (Other os please refer)

    2. activate the project to the project (virtual) env by
    **env/Script/activate on power shell(on other os refer online)

    3. install the dependencies by 
    **pip install -r requirements.txt*

    4. running
    on powershell use command(other shell prese refer)
    $env:FLASK_APP='app.py' and 
    $env:FLASK_DEBUG=true

    ##finally run application backend by
    flask run
    */


## APIS
1. /login
**request body*


Form Fields values

email    c@gmail.com
password   123



**success*
{
  "error": false,
  "user": {
    "email": "c@gmail.com",
    "full_name": "chris",
    "id": 2,
    "password": "123",
    "phone_number": "1234"
  }
}

**error*
{
  "message": "Not Found",
  "success": false
}

2. /register
**request body*


Form Fields values

full_name  chris
email   bundi
password   123
phone_number   1234





**success*
{
  "error": false,
  "user": {
    "email": "c@gmail.com",
    "full_name": "chris",
    "id": 2,
    "password": "123",
    "phone_number": "1234"
  }
}

**error*
{
  "message": "Not Found",
  "success": false
}











