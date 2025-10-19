Task 1: MongoDB Project


Objective:
Create a database called tech_blog_db containing a data structure for a technology blog with schema validation, and populate it with sample data.


Main Requirements

1. Create a database

Database name: tech_blog_db


2. Create three collections with the following structures:

Collection: users
Required fields:
name (string, 2–50 characters)
email (string, valid email format)
it_role (one of the predefined IT roles)
seniority (one of the predefined levels: Junior, Mid, Senior, Lead, Principal)
Optional fields:
join_date (date)
bio (string, max 500 characters)

Collection: posts
Required fields:
title (string, 5–200 characters)
author_id (ObjectId)
content (string, minimum 20 characters)
category (one of the predefined categories)
date (date)
Optional fields:
likes (integer, minimum 0)
tags (array of strings)

Collection: comments
Required fields:
post_id (ObjectId)
user_id (ObjectId)
content (string, 0–200 characters)
date (date)
Optional fields:
likes (integer, minimum 0)


3. Additional Requirements

Define the following constants:
IT Roles: Frontend Developer, Backend Developer, DevOps Engineer, Software Engineer, Data Engineer, QA Engineer, Full Stack Developer
Categories: JavaScript, Python, Java, DevOps, Cloud, Architecture, Best Practices, Testing, Security, Machine Learning, Database
Seniority Levels: Junior, Mid, Senior, Lead, Principal

Create helper functions to generate:
Random integers
Random dates
Random element selection from an array

Generate sample data:
1,000 users
5,000 posts
10,000 comments


4. Implement basic CRUD operations:

Create:
Add a new post

Read:
Find posts by category
Find posts by number of likes

Update:
Single document: update post title and content, and increment likes count
Multiple documents: update likes count for all posts in a given category

Delete:
Remove posts


5. Create aggregation pipelines to show:
Number of posts per IT role
Categories with the highest number of likes
Posts with the highest number of comments


6. Add indexes for query optimization
Create a single-field index in the posts collection
Measure and analyze query execution time before and after creating the index
Create a compound index in the users collection


Good luck! 🚀



Task 2: Amazon DynamoDB


Objective:
Build a catalog system for a multimedia store that stores information about books, music albums, movies, and video games.

Main Requirements
Create a DynamoDB table that stores all products from the above categories.
Insert 3 records for each category (books, music albums, movies, and games).
Retrieve and display:
    The record with product_id = BOOK001
    All records where category = book
    All records where rating = 5
Delete all records where category = game

Table Structure
Table name: MediaProducts-firstname-lastname
Partition key: product_id (String)
    Books: BOOKxxx
    Music albums: MUSICxxx
    Movies: MOVIExxx
    Games: GAMExxx
Sort key: category (String)
Table settings: default

Additional attributes:
title (String)
author_artist (String)
release_year (Number)
price (Number)
genre (String)
language (String)
rating (Number, 1–5)


Good luck! 🚀