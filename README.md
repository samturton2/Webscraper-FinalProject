(Jenkins Test)

# Eng74 Final Project

# MVC - Model View Controller
MVC is a software approach used to organise code. The MVC method establishes 3 silos, the Model, View, and the controller.
  * Controller - receives user requests and decides the action to take. It ties together the Model and View
  * Model - The essential components of code.
   Retrieves data required to respond to controller
  * View - Consists of code pertaining to user interface. This would receive  data from the model and determine which webpage should be rendered to meet the users requests.

# What is Flask
Flask is a python-based web development framework. It provides access to a large collection of reusable code and extensions.

# Jenkins
- A webhook is needed in the git repository.
`<jenkins server url>/github-webhook/`

- The ssh pub key is uploaded to the repo, and private key is used in jenkins to monitor any changes on the development branches.
- Jenkins detects changes and merges with main.

