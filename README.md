# SEA Project ReadMe

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Data Validation](#data-validation)
4. [Models in the Database](#models-in-the-database)
5. [Tests](#tests)
6. [Hosted Version](#hosted-version)
7. [License](#license)

## 1. Project Overview

This Django project is designed to manage tasks, user authentication, and comments. Key components include models for
tasks, users, and comments, as well as forms, views, URL routing, and authentication.

## 2. Project Structure

- `polls/models.py`: Defines the database models for tasks, users, and comments. Each model represents a table in the
  database.
- `polls/views.py`: Includes view functions for handling various aspects of the project, such as user registration,
  login, task creation, and comment submission.
- `polls/templates/`: This directory contains HTML templates used to render the project's web pages.
- `polls/urls.py`: Defines URL routing for the project, mapping URLs to view functions.
- `polls/tests.py`: Defines a suite of tests to ensure the correctness and reliability of the application.

## 3. Data Validation

The project incorporates robust data validation techniques to ensure data integrity and security. Here are some key
aspects of data validation:

- **User Registration**: Validates user input during registration, including password strength checks.
- **Task Creation**: Ensures required fields are filled and applies constraints on data types and lengths.
- **Comment Submission**: Validates comments to prevent issues such as empty comments.

## 4. Models in the Database

The database for this project consists of the following models:

- **Task Model**: Represents tasks with fields for description, assigned user, title, and progress.
- **CustomerUser Model**: Represents user accounts with fields for first name, last name, username, and password.
- **Comment Model**: Represents comments with a "Comment" field.

These models are used to structure and store data in the database.

## 5. Tests

A comprehensive suite of tests has been developed to validate the functionality and behavior of the application. The
test cases cover various scenarios, including successful operations and scenarios that should fail. The tests are
designed to ensure that the application behaves as expected under different conditions, providing confidence in the
reliability of the code.

Here are some examples of the test cases:

- **Login View**: Tests the login functionality with both valid and invalid credentials.
- **Create Comment Form**: Ensures that comments can be created for existing tasks and fails for non-existent tasks.
- **Display Choices**: Outputs all possible choices for the 'Alias_Assigned' field in the 'Task' model.
- **Task Creation**: Tests the task creation functionality, including scenarios where required fields are missing or
  invalid.

These tests can be run to verify the correctness of the application and catch any regressions during development or
deployment.

## 6. Hosted Version

A live version of this project is hosted at [m4llhew.pythonanywhere.com](http://m4llhew.pythonanywhere.com/). You can
access and use the project online.

## 7. License

This project is licensed under the MIT License. See the LICENSE file for details.
