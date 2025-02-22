#Social Media Management System

A robust social media platform designed with modular architecture to allow users to interact with posts, 
comments, and other users. The system also provides an administrative control panel for managing the 
content and users.

Features
	User Management
		Users can register with email and password.
		Users can update their profile information.
	Post Management
		Users can create, edit, and delete their own posts.
		Administrators can block inappropriate posts.
		Posts have likes and favorites.
	Comment Management
		Users can comment on posts.
		Comments can be edited or deleted by their authors.
		Administrators can block comments.
		Likes and Favorites System
		Users can like and unlike posts.
		Users can favorite and unfavorite posts.
	Administration System
		Administrators can block users, posts, and comments.
		Admin Dashboard
		List of registered users.
		List of posts and comments.
	Security
		Passwords are stored using bcrypt hashing.
		Access control based on permissions.
	Database
		Optimized database with indices on foreign keys (FKs).
	Architecture
		Modular architecture for easy future expansion.
		Support for multiple administrators.
	API
		RESTful API with Swagger/OpenAPI documentation.
		Friendly error responses for improved user experience.
		
Technologies Used
	Python: 3.13.2
	PostgreSQL: 17.3
	SQLAlchemy for ORM
