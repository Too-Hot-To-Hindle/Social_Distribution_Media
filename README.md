[![Deploy to Heroku](https://github.com/Too-Hot-To-Hindle/Social_Distribution_Media/actions/workflows/heroku.yml/badge.svg?branch=main)](https://github.com/Too-Hot-To-Hindle/Social_Distribution_Media/actions/workflows/heroku.yml)

# Social_Distribution_Media

See below section **Project Part 1 Summary** for project progress thus far.

[Deployed App](https://social-distribution-media.herokuapp.com/) | [API Documentation](https://social-distribution-media.herokuapp.com/api/schema/swagger-ui/)

[Project implementation](https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org) of a social network using the inbox model.

## Running Instructions

Our app uses a React frontend and Django backend. The frontend code is built and copied to the `backend/build` directory, which is served when running the Django app.

When making changes, the new version is automatically built and depolyed to Heroku by a [github action](https://github.com/Too-Hot-To-Hindle/Social_Distribution_Media/blob/main/.github/workflows/heroku.yml).

### React Setup

#### Install packages

`cd frontend`

`npm install`

#### Copy build files to Django project

`npm run relocate`

This will build the app and copy the `/build` folder to `/backend/build`, where Django will serve it.

> **_NOTE:_** You can also use `npm run start`, but this won't have access to the backend

### Django Setup

#### Virtual Environment

`cd backend`

Create a virtual environment

e.g. `virtualenv venv`

Activate the environment

`. venv/bin/activate`

Install all the required packages

`pip install -r requirements.txt`

#### Local DB

Run intial migrations

`python manage.py migrate`

Create Superuser

`python manage.py createsuperuser`

#### Run App

`python manage.py runserver`

-----

# Project Part 1 - Summary

## Total Project
- Current state of project is deployed and functional on [Heroku](https://social-distribution-media.herokuapp.com/).
- Basic auth is required to make requests to our API for endpoints where required, and frontend relies on some cookies/local storage objects to make requests where needed. Currently in a proof of concept stage, will be reinforcing in later project parts.
- **21/43** user stories completed (both frontend and backend), with progress made towards multiple others:
    - As an author, I want to like posts that I can access.
    - As an author, I want to befriend local authors.
    - As a server admin, I want a restful interface for most operations.
    - As an author, when I befriend someone (they accept my friend request) I follow them, only when the other author befriends me do I count as a real friend – a bi-directional follow is a true friend.
    - As an author, I want to know if I have friend requests.
    - As an author, I want to use my web browser to manage my profile.
    - As an author, my server will know about my friends.
    - As an author, I want to be able to delete my own public posts.
    - As a server admin, I want to host multiple authors on my server.
    - As an author, I want to be able to use my web browser to manage/author my posts.
    - As a server admin, I want to be able to add, modify, and remove authors.
    - As an author, I want to make public posts.
    - As an author, posts I create can link to images.
    - As an author, I want to edit public posts.
    - As an author, posts I make can be in plain text.
    - As a server admin, images can be hosted on my server.
    - As an author, posts I create can be images.
    - As an authors, posts I create can be in CommonMark.
    - As an author, I want to be able to make posts that are unlisted, that are publicly shareable by URI alone (or for embedding images)
    - As an author, I want to comment on posts I can access
    - As an author, other cannot modify my public posts

    - **Progress made towards the following other user stories:**
        - As an author, posts I create can be private to another author (frontend began, backend/auth work continuing)
        - As an author, posts I create can be private to my friends (frontend began, backend/auth work continuing)
        - As an author, I should be able to browse the public posts of everyone (technically possible, but Search feature in frontend doesn't query posts yet, so it's a little inaccessible without URIs)
        - As an author, comments on friend posts are private only to me the author (comments functionality largely begun, need to add user scopes in backend)
        - As an author, I want un-befriend local and remote authors (backend for local friend removal set up, need to integrate in frontend)
        - As an author, when someone sends me a friends only-post I want to see the likes (backend for likes setup, still need to setup scopes, need to integrate in frontend)
        - As an author, I want a consistent identity per server (local server identity setup)

## Code Base
Code base and project structure is cleanly organized, with frontend and backend aspects of projects sitting in `frontend/` and `backend/` respectively. As per development environment configration instructions in `README.md`, project can easily be cloned and run locally using the `Makefile`.

## Test Cases
Postman tests (not just the endpoints -- but tests that are run on each execution too!) are setup for the majority of endpoints currently setup for the above completed and in-progress user stories. We have also begun writing unit and UI tests, in `backend/tests` and `frontend/src/App.test.js` respectively.

An export of our Postman collection can be found in [`postman_collection.json`](./postman_collection.json).

## UI
UI is cleanly organized, and provides multiple loading and status indicators. Progress made in frontend in tightly couple with progress made in backend, with a few extra strucutal pieces setup in the frontend for look and feel that we'll later integrate. A Figma diagram has been planned out and created in `UI Design Mockups.png`. 

## Tool Use
GitHub has been extensively used, majorily for version control, but also through the use of GitHub Issues and Projects to track user stories progress. All group members have made contributions to the repository for this project part. Our Heroku project architecture has already been stood up, and functional with a GitHub Actions CI/CD pipeline. 

## TA Demo
Yet to come!

## Web Service API & Documentation
Backend project strucutre is cleanly organized all in the `backend/` directory, with comments. Open API specification exists and has examples, and can be found (deployed) [here](https://social-distribution-media.herokuapp.com/api/schema/swagger-ui/).

## Design
Overall project has been designed with simplicity and ease of use in mind, pulling inspiration from other popular social networking sites. Plans were created and followed for frontend development, and backend development for this project part was designed to follow as closely to spec as possible with careful consideration for feature extension. 

-----

# Project Part 2 - Summary
## Total Project
- Current state of project is deployed and functional on [Heroku](https://social-distribution-media.herokuapp.com/).
- Connected to 2 groups (a cloned instance of our project, and group 11's) with partial progress on a connection to group 6
- All remote-functionality-required endpoints are integrated in frontend
- All pagination-required endpoints are now configured to spec
- All-new proxy functionality is configured in backend to faciliate remote connections
- Caching is scaffolded and ready to go for remote connections -- just need to decide on a max-age/reconnection strategy, and our backend makes local copies of objects sent to us

- **31/43** user stories completed (both frontend and backend), with progress made towards multiple others:
    - As a server admin, I want to share public images with users on other servers.
    - As an author, I want to befriend remote authors.
    - As a server admin, I don't want to do heavy setup to get the posts of my author's friends.
    - As a server admin, I want to be able to add nodes to share with.
    - As a server admin, I want to be able to remove nodes and stop sharing with them.
    - As a server admin, node to node connections can be authenticated with HTTP Basic Auth.
    - As a server admin, I can limit nodes connecting to me via authentication.
    - As a server admin, I can disable the node to node interfaces for connections that are not authenticated!
    - As an author, I want a consistent identity per server.
    - As an author I should be able to browse the public posts of everyone.
    - As an author, I want to like posts that I can access.
    - As an author, I want to befriend local authors.
    - As a server admin, I want a restful interface for most operations.
    - As an author, when I befriend someone (they accept my friend request) I follow them, only when the other author befriends me do I count as a real friend – a bi-directional follow is a true friend.
    - As an author, I want to know if I have friend requests.
    - As an author, I want to use my web browser to manage my profile.
    - As an author, my server will know about my friends.
    - As an author, I want to be able to delete my own public posts.
    - As a server admin, I want to host multiple authors on my server.
    - As an author, I want to be able to use my web browser to manage/author my posts.
    - As a server admin, I want to be able to add, modify, and remove authors.
    - As an author, I want to make public posts.
    - As an author, posts I create can link to images.
    - As an author, I want to edit public posts.
    - As an author, posts I make can be in plain text.
    - As a server admin, images can be hosted on my server.
    - As an author, posts I create can be images.
    - As an authors, posts I create can be in CommonMark.
    - As an author, I want to be able to make posts that are unlisted, that are publicly shareable by URI alone (or for embedding images)
    - As an author, I want to comment on posts I can access
    - As an author, other cannot modify my public posts

    - **Progress made towards the following other user stories:**
        - As an author, posts I create can be private to another author (frontend began, backend/auth work continuing)
        - As an author, posts I create can be private to my friends (frontend began, backend/auth work continuing)
        - As an author, I should be able to browse the public posts of everyone (technically possible, but Search feature in frontend doesn't query posts yet, so it's a little inaccessible without URIs)
        - As an author, comments on friend posts are private only to me the author (comments functionality largely begun, need to add user scopes in backend)
        - As an author, I want un-befriend local and remote authors (backend for local friend removal set up, need to integrate in frontend)
        - As an author, when someone sends me a friends only-post I want to see the likes (backend for likes setup, still need to setup scopes, need to integrate in frontend)
        - As an author, I want a consistent identity per server (local server identity setup)
        - As an author, when someone sends me a friends only-post I want to see the likes. (technically done, need to work on scopes still though)
        - As an author, I can share other author's public posts. (technically done, need to work on scopes still though).
        - As an author, I can re-share other author's friend posts to my friends. (technically done, need to work on scopes still though).

## Web Service API & Documentation
Backend project strucutre is cleanly organized all in the `backend/` directory, with comments. Open API specification exists and has examples, and can be found (deployed) [here](https://social-distribution-media.herokuapp.com/api/schema/swagger-ui/). All requests now include example request bodies (if applicable), example responses + response codes, and are specically tagged if they make use of the new remote-proxy functionality or pagination.

## Web Service Coordination

The following endpoints are confirmed to be working with our **cloned instance**:

- GET All Authors ✅
- GET Single Author ✅
- GET Author Followers ✅
- GET Check If Follower ✅
- GET Single Post ✅
- GET Author Recent Posts ✅
- GET Check If Image Post ✅
- GET Post Comments ✅
- GET Post Likes ✅
- GET Comment Likes ✅
- GET Author Liked ✅
- POST Send Post ✅
- POST Send Follow Request ✅
- POST Send Like ✅
- POST Send Comment ✅

The following endpoints are confirmed to be working with **Group 11's instance**:

- GET All Authors ✅
- GET Single Author ✅
- GET Author Followers ✅
- GET Check If Follower ✅
- GET Single Post ✅
- GET Author Recent Posts ✅
- GET Check If Image Post ✅
- GET Post Comments ✅
- GET Post Likes ✅
- GET Comment Likes ✅
- GET Author Liked ✅
- POST Send Post ✅
- POST Send Follow Request ✅
- POST Send Like ✅
- POST Send Comment ✅

The following endpoints are confirmed to be working with **Group 6's instance**:

- GET All Authors ✅ (not integrated into frontend at this time, it's in our Postman collection)

## Design
Overall project has been designed with simplicity and ease of use in mind, pulling inspiration from other popular social networking sites. Plans were created and followed for frontend development, and backend development for this project part was designed to follow as closely to spec as possible with careful consideration for feature extension. 

One particular piece from this project part that plays into this design mantra is the backend proxy feature set. Detailed further on this [Notion document](https://www.notion.so/Project-Part-2-4baf94b2e18e4bf8a57fa2b98f7a91de?pvs=4), the proxy feature allows requests to be made to the backend where an applicable author ID properly URL encoded for a remote server node passed in as a path parameter to a supported endpoint has the backend communicate with the remote node, parse and serialize responses properly matching their spec, and patches back the response as if you were asking only our server. This greatly faciliated remote integration with our frontend application -- since the endpoint to search all authors was the only one that needed a specially developed endpoint -- and the rest just worked in integration. 

-----

# Project Part 3 - Summary
## Total Project
- Coordinates and connects with 4 other groups and a cloned instance of our own server. 
- Posts with embedded images (via Markdown) are visible.
- Image posts are visible.

## Code Base
- 90% of requirements are implemented. Code is clean and commented where necessary. 
- 41/43 = 95.34%. With this, we allowed some buffer in case of a random bug or another groups connection goes dark so that we remain above the 90% threshold.
- **41/43** user stories completed (both frontend and backend), with progress made towards multiple others:
    - As a server admin, I want to share public images with users on other servers.
    - As an author, I want to befriend remote authors.
    - As a server admin, I don't want to do heavy setup to get the posts of my author's friends.
    - As a server admin, I want to be able to add nodes to share with.
    - As a server admin, I want to be able to remove nodes and stop sharing with them.
    - As a server admin, node to node connections can be authenticated with HTTP Basic Auth.
    - As a server admin, I can limit nodes connecting to me via authentication.
    - As a server admin, I can disable the node to node interfaces for connections that are not authenticated!
    - As an author, I want a consistent identity per server.
    - As an author I should be able to browse the public posts of everyone.
    - As an author, I want to like posts that I can access.
    - As an author, I want to befriend local authors.
    - As a server admin, I want a restful interface for most operations.
    - As an author, when I befriend someone (they accept my friend request) I follow them, only when the other author befriends me do I count as a real friend – a bi-directional follow is a true friend.
    - As an author, I want to know if I have friend requests.
    - As an author, I want to use my web browser to manage my profile.
    - As an author, my server will know about my friends.
    - As an author, I want to be able to delete my own public posts.
    - As a server admin, I want to host multiple authors on my server.
    - As an author, I want to be able to use my web browser to manage/author my posts.
    - As a server admin, I want to be able to add, modify, and remove authors.
    - As an author, I want to make public posts.
    - As an author, posts I create can link to images.
    - As an author, I want to edit public posts.
    - As an author, posts I make can be in plain text.
    - As a server admin, images can be hosted on my server.
    - As an author, posts I create can be images.
    - As an authors, posts I create can be in CommonMark.
    - As an author, I want to be able to make posts that are unlisted, that are publicly shareable by URI alone (or for embedding images)
    - As an author, I want to comment on posts I can access
    - As an author, other cannot modify my public posts
    - As an author, I can share other author's public posts.
    - As an author, I can re-share other author's friend posts to my friends.
    - As an author, posts I create can be private to another author
    - As an author, posts I create can be private to my friends
    - As an author, I should be able to browse the public posts of everyone
    - As an author, I want a consistent identity per server
    - As an author, I want to post posts to my "stream"
    - As an author, comments on friend posts are private only to me the author
    - As an author, I want un-befriend local and remote authors
    - As an author, when someone sends me a friends only-post I want to see the likes
    - As an author, when someone sends me a friends only-post I want to see the likes.

- **User stories left out since we hit 90% threshold:**
    - As a server admin, I want to optionally be able to allow users to sign up but require my OK to finally be on my server
    - As an author, I want to pull in my GitHub activity to my stream

## UI
- UI is tested and works well, integrates with our user stories nicely. 
- Planning remains tied to our Figma diagram we put together in the first project part. 

## Web Service Coordination
- Web service proxy functionality is in its final form, with caching functionality built-in if needed.
- Connection to the web service of:
    - a cloned deployment of our web service
    - Group 6's service
    - Group 10's service
    - Group 11's service
    - Group 13's service
- The following endpoints were tested and confirmed to work with each:
    - GET All Authors ✅
    - GET Single Author ✅
    - GET Author Followers ✅
    - GET Check If Follower ✅
    - GET Single Post ✅
    - GET Author Recent Posts ✅
    - GET Check If Image Post ✅
    - GET Post Comments ✅
    - GET Post Likes ✅
    - GET Comment Likes ✅
    - GET Author Liked ✅
    - POST Send Post ✅
    - POST Send Follow Request ✅
    - POST Send Like ✅
    - POST Send Comment ✅

## Web Service API & Documentation
- Documented is linked aboved; has been updated over the course of the sprint with new functionality. 
- Examples are included where required (ie. for POST requests) -- most notably for the POST /inbox endpoint, where it can be ambiguous between groups the request body format.

## Test Cases
- Test cases exist for both backend (using the built in Django test runner), frontend (using Jest), and in our Postman collection.

## Tool Use
- Git was consistently used for CI/CD, collaboration, and organization.
- Pull requests were used for larger changes to codebase.
- GitHub Project board and Issues are up to date with project progress.

## Design
- Both backend and frontend followed tried and true design patterns.
    - Backend most notably followed an object-oriented-esque pattern designing serializers for remote connections.
    - Frontend most notably followed a page-by-page and reusable component design.

## Adhering to Standards
- All endpoints with sample request responses and request bodies were implemented as written in original project documentation. 
- Remainder of endpoints were written in an attempt to futher follow this model (most evidently seen in the POST /inbox examples, where an example was given for follow requests, and we tried to follow this for likes, comments, and posts by including the whole object in the object field).

## Addresssing Feedback
- We made an effort to follow advice from TA over course of semester -- tried some new things with our serializer classes but ended up sticking to our orignal design pattern.
- Followed his advice for some React best practice, helped with some react-router-dom related things.

## Presentation
- Within time, outfits coordinated, bananaman theme followed, showed teamwork, followed practiced script, and promoted our application!

## Video Demo
- Can be found [here](https://youtu.be/OnOKN7GfFXU), on YouTube.
- Under 2 minutes, showing off most critical functionality of application.

## AJAX
- Uses AJAX everywhere in frontend, thanks to React and its useState hooks.
- Little instances where a page reload is required.