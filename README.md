# Track your calories
Application for keeping track of the calories and other nutrients you eat.

It was created as a project for Scripting Langages subject at Wrocław University of Sience.

## Funcionalities:
- creating users, each user has its own history
- setting parameters of the user, such as height, weight, age, limits for paritcular nutrients
- searching through the product database and saving those, which have been eaten
- creating own products with all the neutrients filled by hand
- creating own products combinded out of other products 
- searching through own eat history
- displaying a graph showing th consumption of selected neutrinet in last days

## Technologies:
- all the information about the products comes from nutritionix API. To communicate with it program uses the request library
- pickle library is used for saving all the data for each user
- for creating a GUI prgram uses the PySide6 library
- for displaying graphs program uses seaborn and matplotlib libraries


## Requirements:

All the library requirements are spicified in the requirements.txt file. 

To connect with the API program requires an API key and app ID. They are not on the github for security reasons. Key and id should be saved in a file *headers.json* in the following format:

`{"x-app-id": "YOUR_APP_ID", "x-app-key": "YOUR_API_KEY"}`
