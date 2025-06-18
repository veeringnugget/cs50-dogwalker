# FETCH
#### Video Demo:  https://www.youtube.com/watch?v=OQJwZs8CXxg
#### Description:
Fetch is my CS50x Final Project - a platform designed for dog-walkers to manage their clients, track walks and monitor payments, all in one place.

I noticed that many dog-walkers rely on informal methods like Facebook groups or personal websites to oragnise their business. Fetch aims to streamline this process, offering a scalable solution with separate roles for walkers and clients that could be added further down the line.

Login:
The login page is designed to be clean and modern with some personality added through the imagery on the left. I used Flask's flash functionality to display helpful error messages for missing or incorrect login details. This helps to guide users without disrupting the user experience.

Register:
The registration page follows the same clean design as the login. It also uses flash messages to provide instant feedback on user input errors. 

Index / Homepage:
This was the most challenging page to build. I chose to use Boostrap for layout and styling to help ensure consistency, but I struggled with the left-hand sidebar navigation and the responsiveness of the layout across different screen sizes. My initial vision was to show more detailed information up front, but I pivoted towards a simpler, dashboard-style layout that offers a quick snapshot of a walkers activity.

The index / homepage has 4 main panels:
1. Client Tracker -> Displays all clients associated with the logged-in walker, including pet's name, breed, age, gender and any notes.
2. Walk Tracker -> Logs all walk activity, including the type of walk or session and the duration.
3. Payments -> Shows each client's payment status - how much was charged and whether or not it had been paid.
4. General Overview -> Offers an aggregated summary, including the total number of paid vs unpaid sessions and a client count. A limitation here is that multiple dogs per client are not fully differentiated, which may cause confusion in interpreting client totals.

Whilst the layout could be improved with more time and experience, I'm glad I managed to capture the main features I originally intended.

Walks:
This page is used to log and track walk details. I used a for loop to iterate over the client list, displaying both the pets name and the breed to help avoid confusion if there are multiple pets with the same name. The form contains dropdwons and inputs that a walker would typically use - type of walk, duration, payment amount, etc.

All data here is stored in the walks table of fetch.db. It also links each walk to a specific client using a foreign key, enabling seamless connection across different parts of the application.

Add a Client:
This is where the walker will add any clients they have on their books and again, it is a simple form for them to fill out and it will add to a table named "clients". Throughout my tables, I ensured to keep a Primary Key and a Foreign Key to ensure that all tables were able to be interconnected so that they could all work together.

This page allows walkers to register a new client. The form is kept simple to allow to allow fast input, collecting details such as the client's name, pet's name, breed, age, gender, and any additional notes. Information submitted is stored in the clients table.

Each client is assigned a unique primary key, and every entry is tied to the logged in user via a foreign key. This structure keeps all user data separated and allows multiple users to have their own sets of clients without overlap or data leakage.

Database Structure:
The project uses SQLite with the following tables:
1. users - stores the user login details
2. clients - stores client and pet information
3. walks - stores walk details, linked to clients

Conclusion:
Overall, I'm proud of what I achieved with Fetch. This project brought together many of the skills I learnt through CS50x - Flask, Jinja, HTML/CSS, Python, SQL and Bootstrap into a useable application. It is the first time I have built something from scratch with a backend and frontend that work together.

There are definitely areas that could be improved upon. However, I now have a deeper understanding of full-stack web development and where I need to look at next. If I was to look at Fetch again, I would improve the responsiveness and build out client-facing functionality.