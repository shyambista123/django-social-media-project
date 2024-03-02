# Simple Social Media Web App

## Project Overview

The Simple Social Media Web App is a Django-based web application designed for intuitive social interactions. It includes features such as user registration, email verification, profile management, post creation, and social interactions like liking, commenting, and following/unfollowing users.

## Key Features

1. **User Registration and Verification:**
   - New users can register with essential information.
   - Email verification ensures account authenticity.

2. **Authentication and Authorization:**
   - Secure user authentication for account confidentiality.
   - Password reset functionality via email.

3. **Profile Management:**
   - Personalize profiles with pictures and bios.
   - Password change and account deletion for security.

4. **Post Management:**
   - Create, edit, and delete posts with images and text.

5. **Social Interactions:**
   - Like posts to express appreciation.
   - Comment on posts for communication.
   - Follow/unfollow other users for social connections.

## Technology Stack

- **Django Framework:**
  - Provides a robust and scalable architecture.

- **PostgreSQL Database:**
  - Utilized for storing user data and post information.

- **Bootstrap:**
  - Ensures a responsive and visually appealing user interface.

# Project Setup Instructions

## Maildev Configuration:
1. Clone project: `git clone https://github.com/shyambista123/django-social-media-project.git`
2. Navigate to the project directory: `cd django-social-media-project`
3. Install project dependencies: `pip install -r requirements.txt`
4. Install Maildev using: `npm install maildev`
5. Start Maildev with: `maildev`
6. Access the Maildev interface in your browser at: [http://0.0.0.0:1080/](http://0.0.0.0:1080/)

Make sure to perform these steps before testing the project, as Maildev is used to send emails for verifying users. This ensures the confirmation of user identities and activation after registration.
