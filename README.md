# The Originals test task

*To start the project you need to execute:**

* clone project repo
* Create an .env file and populate it following the default.env file example

* execute the command `make build`
* execute the command `make cmd`
* execute the command `make run`

You can fill db or run `make load` for load dump (**when container is running**)

you can check swagger on http://0.0.0.0:8080/docs


you can create user on route: POST http://0.0.0.0:8080/auth/sign-up

or use user from dump:

*users creds for testing:*
* user with user role: username:"stringst22", password:"stringst"
* user with manager role: username:"usermanager", password:"usermanager1"
* user with admin role: username:"useradmin", password:"useradmin"


if you *Admin* you can: 

* create tasks and read, update, delete all tasks

if you *Manager* you can: 

* create and read all tasks 
*  update, delete tasks where you are responsible person

if you *User* you can: 

* read all tasks 
* Update status on tasks where you assignee


*P.S*

What I would improve with time:
* I would put tokens in Redis by adding user sessions;
* I would add routines for the user (edit profile, change password, etc.);
* I would expand the functionality of roles;
* I would add sending an email as a delayed task