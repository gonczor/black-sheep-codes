![Build](https://github.com/gonczor/black-sheep-learns/workflows/Test/badge.svg)

# Black Sheep Learns

This contains source code for learning platform. Currently it is in development phase.

Project currently relies on Django and Django Rest Framework with PostgreSQL as database, in the nearest future proper frontend will be implemented, preferrably using Vue.js framework.

# Architecture

This is a monolithic service that exposes both frontend stuff and RESTful API. Fronetend stuff can be found in `src/frontend` directory. API calls are made under `/api/v1/<endpoint>`. Currently they are undocumented.

# Project setup

## Prerequisites

You need to know Python or JS and have docker-compose installed.

## Steps

 1. Copy `.env.example` file to `.env`. It should contain all necessary variables set for local development.
 2. Run docker-compose up. By default it will start Django's development server that you can access on `http://localhost:8000/`

## Testing

Run `docker-compose run web python manage.py test`.

## Deployment

Project is set up to be deployed automatically on AWS architecture after each push to the `master` branch.

# Contributing

I am not going to pretend this isn't going to be a commercial project. While I'm very much in favor of open source, I'm also going to turn this into a commercial project. I know that some people may dislike this, so I want to make it very clear from the beginning.

Nonetheless, since this is an open source project, you may still submit Pull Requests and I'll be happy to review them. You might go through the Issues page to search for "Good first issue" if you are looking for something simple. I'm working on it in my spare time, so I may be slow to respond, but I'm happy to share my knowledge and help those, who want to help me. If you want to learn something new - go ahead :-)
