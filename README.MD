# _Superhero API_

#### By _**Jarret Jeter**_

#### _An API project using both GET and POST methods for a database with superheroes_

## Technologies Used

* _Python_
* _Pandas_
* _Flask_
* _Postman_

## Description

_I created a small database on a local server with a few superheroes that I like which my API can connect to. Using the correct queries for the "/see_stats" endpoint, my API can read the entire superhero dataframe or just a select few superheroes via a GET method and return it as a json object. With "/add_stats" my API creates a json object to add to the database using a POST method if all required information is input_

## Setup/Installation Requirements

* _Make sure you have a text editor such as Visual Studio Code installed.
* _Clone this repository (https://github.com/jarretjeter/Superhero-API.git) onto your local computer from github_
* _Open your terminal, go to the directory where you cloned the repository and create a virtual environment with Python3.7 installed and "pip install -r" the requirements.txt in that environment_
* _Run the main.py file_
* _In postman, create a workspace and open a request tab_
* _Copy your local server ("http://127.0.0.1:5050" + "/see_stats") into the postman request url with the GET method selected and click Send_
* _From there you are given back the current superheroes in the database and can add more via the POST method and "/add_stats" with a correct json object input into the body section_

## Known Bugs

* _No known bugs at this time_

## License

_If you have any questions, please email me at jarretjeter@gmail.com_

[MIT](https://github.com/jarretjeter/Superhero-API/blob/main/LICENSE.txt)

Copyright (c) _5/27/2022_ _Jarret Jeter_