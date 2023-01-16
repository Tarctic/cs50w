# escape

Point-and-click escape game

[YouTube](https://www.youtube.com/watch?v=VIXXDsf2XkE) |
[Project Specification](https://cs50.harvard.edu/web/2020/projects/final/capstone/)

Implements:
- Login System
- New Game / Continue (saves progress)
- The actual game ([More below](https://github.com/Tarctic/cs50w/tree/main/capstone#detailed-working-of-the-games-js-code))

Uses:
- Django
- HTML
- CSS
- Python
- JavaScript (React)

---

### Introduction:

I've been working on the project for quite a while, especially the layered, complex js of the game's functionality. My original plan was to create an elaborate game with subtle clues, and this was only supposed to be a prototype to see if all those elements worked which I planned to include in the main game. However, this ended up taking way more time than expected with university and other courses, and I realized I had to complete it before the time ended (I started CS50w last June!). However, I plan to continue to create the original game at my own pace. If this project fails, I hope I can receive clear feedback, so that I can improve in those areas.

---

### What's contained in each file:

#### JS files:
- *game.js*:

    Main functionality of the game.

    Contains nearly all the code of the game's working. [Full description](https://github.com/me50/Tarctic/edit/web50/projects/2020/x/capstone/README.md#detailed-working-of-the-games-js-code) is given below.

#### Python files:
- *views.py*:

    Contains code to login, logout and register the user and the background part of saving the game. Sends information back and forth to database and js files.

    Contains five views:
    1. index: Loads the main page along with id and username of the user which are needed in the game.js file.
    2. login_view: Collects username and password from POST request and uses authenticate() method to check if the username exists and if the password is correct. If the method returns a User object, the user is redirected to the index page. Otherwise, if it returns None, an error message is shown. If the request is not a POST request, the login page is rendered again.
    3. logout_view: Logs the user out using logout() method, then redirects the user to the main page.
    4. register: Collects username, email, password and password confirmation from POST request and then checks if the password confirmation matches the password entered. If it does not, then an error message is shown. If it does, a User object is created and saved. If the the username already exists, the user is notified about the error. Then, a Profile object is created and saved using the previously created User object as foreign key identifier. The user is then logged in and redirected to the main page. If the request is not a POST request, the register page is rendered again.
    5. save: The Profile object of the current user is retrieved from the database. If the retrieval fails, then an error message is shown. If the request method received is GET, then the value of the progress variable of the current user's Profile object is sent to the game.js file using JsonResponse() method. 

    If the request method is POST, the progress number sent through fetch request from game.js is collected and saved to the user's Profile object. A HttpResponse indicating success is then returned. 


- *models.py*:

    Contains two models:
    1. User: Uses AbstractUser to create a custom User model instead of the default one.
    2. Profile: Contains a foreign key attribute pointing to a User object and another attribute that stores a value indicating user progress.
- *urls.py*:

    Contains the urlpattens list storing five url paths for the main page, logging in, logging out, registering user and saving progress.

#### CSS files:
- *styles.css*:

    Contains code for styling elements and making them more responsive in html and js files.
#### HTML files:
- *layout.html*:

    Template for other html files.

    Contains links for styles.css, bootstrap, react, babel, and fonts along with csrf_token in the head section. 

    In the body section, the basic design of the website is implemented with links to different parts of the website.
    
- *index.html*:

    Main page of the website where the code contained in game.js runs.
- *login.html*:

    Interface for user to login. 

    Contains a form that asks for username and password along with a submit button. A div is placed to display any error. A link to the register page is given at the bottom for those who do not have an account.

- *register.html*:

    Interface for user to register.

    Contains a form that asks for username, email, password and password confirmation along with a submit button. A div is placed to display any error. A link to the login page is given at the bottom for those already have an account.    

---

### Distinctiveness and Complexity:

Escape is neither a social network nor an e-commerce site, but is a site for a point-and-click escape game. The main complexity of the website lies in the JavaScript code of the game, which largely contains the game's functionality. The JS code contains images, states containing lists, functions to add and remove from the list onclick, a login system, all organized in a very complex mapping of objects that rely on one another. 

Here is a flowchart depicting the structure of the site:

![Flowchart](https://user-images.githubusercontent.com/85291498/168768326-6bebc66b-a3c1-4ed6-bac8-d8ce4f6136ea.jpg)


Given below is the thorough explanation of the JS code.

#### Detailed working of the game's JS code:

The primary component in the JS file is &lt;App /&gt; which contains two smaller components &lt;Start /&gt; and &lt;Main /&gt; for the start menu and the main game respectively. Start menu has 3 buttons: New Game, Instructions and About. If the user is anonymous, a 'Login' button is included. If the user is logged in and has saved progress, a 'Continue' button is included. 

<img width="334" alt="image" src="https://user-images.githubusercontent.com/85291498/164957362-516a1f2a-abb4-4eab-959a-1ec54d6121f1.png">

On loading the main page, a fetch request is sent to get the user progress, if user is logged in. This is to determine which buttons to display on the main menu and for setting the right panel, which will be explained below. Only the &lt;Start /&gt; component is loaded first. After it has loaded, if the user is logged in and clicks 'New Game', &lt;Main /&gt; component is loaded, which sets the game state to 0, which means that the game will start from the beginning. 


A panel is essentially a combination of a background with images that represent objects. 
When &lt;Main /&gt; is loaded, the background and all the objects of panel 1 of the game is loaded. The background variable is stored in a state and a single background div accesses this state. When a specific button or div is clicked, the state is changed, which then changes the classname of the div, thus changing the background. 

<img width="295" alt="image" src="https://user-images.githubusercontent.com/85291498/164957457-68f4fe5b-41ca-4699-a93f-3fc502249d7b.png">



Similarly, another state holds a list of string values, each corresponding to an object in the game. If the object name is included in the state, the corresponding div or button is loaded with a classname pointing to its css. All interactable objects have an onclick function, which then triggers other functions to add/remove objects to/from the screen (delAddObj), add/remove items to/from the inventory (addToInv, delFromInv) or to change the panel (panel1, panel2 etc.). 

<img width="467" alt="image" src="https://user-images.githubusercontent.com/85291498/164957490-02634917-bcaa-46c9-ae61-6f38947e35c0.png">
<img width="560" alt="image" src="https://user-images.githubusercontent.com/85291498/164957508-5d1b7307-3deb-4578-8ebb-0401305a49ea.png">

Objects also include speech bubbles. Speech bubbles have additional states such as text and speaking and a function (say) which implements both. Text state is to use multiple phrases in the same div and speaking state is to determine whether there already is a speech bubble, so that only one speech bubble is displayed at a time. However, the function say() uses delAddobj function, and for some reason, this function cannot be repeated twice in the same onClick. This is why those divs which already call delAddObj(), use setText spearately instead of using say().

<img width="246" alt="image" src="https://user-images.githubusercontent.com/85291498/164957766-ffe3467e-5869-4591-87e5-d8a569d72768.png">
<img width="394" alt="image" src="https://user-images.githubusercontent.com/85291498/164957963-86f52423-90e9-441f-b632-cf4dbd493e31.png">

The inventory is part of the objects list, but it has a state of its own in order to control the objects stored and removed from it. The list in its state is put through the map() function which iterates over each item stored in the state and displays it using classnames. The inventory also has functions of its own that add/remove items to/from the inventory. If an item in the inventory is in use, the cell it occupies is highlighted by editing the classname.


<img width="319" alt="image" src="https://user-images.githubusercontent.com/85291498/164957819-7422b8a9-a260-47cd-81fb-3092a7fa018f.png">
<img width="321" alt="image" src="https://user-images.githubusercontent.com/85291498/164957833-bf9cf9ca-eeac-47c5-82b5-0d9ee974b5b6.png">

The game also includes a form to submit answer entered by the user in one part of the game. The entered answer is then compared with the actual answer, and if it is right, another function is called which displays the end of the game.


The ending displays a GIF with a timeout of 10 seconds matching the end of one loop in the GIF. After the timeout, the GIF is replaced by an image along with a button to go back to main menu.

<img width="142" alt="image" src="https://user-images.githubusercontent.com/85291498/164957536-bbecf3b3-77bf-47a3-b83e-a63f81c6bf38.png">

If a logged in user closes the game at any point, they can continue from where they left off the next time they play. This is thanks to the concept of panels. A POST request with a number indicating the progress is sent. POST requests are sent everytime anything significant to the progress of the game is encountered (such as obtaining the key). When the user clicks continue, the panel, that is, the background and objects relevant to their progress number is returned. If 'New Game' is clicked, the previous progress is overwritten by sending another POST request with '0' indicating that the user is playing from the beginning. 

---

#### Additional information:
Sometimes, in-game objects require multiple clicks to respond.
