# Typhoon-Monitoring-System
Final Project for Database Course in Tongji University 2024

A web-based **Typhoon Monitoring and Information Management System** designed to enhance real-time tracking, analysis, and early warning of typhoon events. Built with **Flask** and **MySQL**, the platform serves as a reliable and accessible tool for both **meteorological agencies** and **general users** to manage, query, and visualize typhoon data.


### 1. Project Overview

#### Background

With the increasing frequency and intensity of climate-related disasters, **typhoon monitoring** has become a crucial task for disaster prevention and mitigation. This system integrates **meteorological science** with **information technology** to establish a platform for **real-time typhoon tracking, prediction, and information dissemination**.

The system enables meteorological departments to manage comprehensive typhoon data, while providing the public with up-to-date information and alerts to enhance preparedness and reduce potential damages.

#### Objective

The project aims to:

* Provide **real-time monitoring** of typhoon formation, intensity, and path.
* Enable **data-driven decision-making** for meteorological authorities.
* Offer **public access** to accurate and dynamic typhoon information.
* Support **subscription and notification services** for personalized updates.


### 2. Features

| Category                    | Description                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------ |
| **User Management**         | Registration, login, and role-based access (Admin / General User).                               |
| **Typhoon Data Management** | CRUD operations on typhoon records including location, time, longitude, latitude, and intensity. |
| **Search & Query System**   | Flexible search filters by typhoon ID, region, date, or landfall location.                       |
| **Subscription System**     | Users can subscribe to specific typhoons and receive real-time updates.                          |
| **News & Notifications**    | Admins can publish, edit, or delete news; users can view and discuss alerts.                     |
| **Visualization**           | Interactive typhoon path maps and dynamic data visualization.                                    |

### 3. System Architecture

The system follows a **non-separated architecture**, where Flask handles both backend processing and frontend rendering.

```
User Interface (HTML/CSS/JS)
         │
         ▼
Flask Framework (Routing + Logic)
         │
         ▼
SQLAlchemy ORM → MySQL Database
```

* **Frontend:** HTML templates rendered by Flask with Jinja2.
* **Backend:** Flask routes and controllers for logic and data flow.
* **Database Layer:** SQLAlchemy ORM ensuring secure and efficient data operations.


### 4. Database Design

The system’s database is based on a **relational model** that adheres to **Third Normal Form (3NF)**, minimizing redundancy and maintaining integrity.

#### Main Entities

| Entity                 | Description                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------ |
| **Manager_user**       | Stores admin credentials and metadata.                                               |
| **Common_user**        | Stores general user account information.                                             |
| **Typhoon_basic_info** | Core typhoon data including ID, location, time, longitude, latitude, and popularity. |
| **News**               | Stores notifications and public announcements.                                       |
| **Subscribe**          | Maps users to their subscribed typhoons and timestamps.                              |

Each entity has a **primary key**, and all non-key attributes fully depend on it, ensuring normalization and consistency.


### 5. Technical Stack

| Layer                 | Technology                                     |
| --------------------- | ---------------------------------------------- |
| **Frontend**          | HTML, CSS, JavaScript, Jinja2, AJAX            |
| **Backend**           | Python, Flask, Flask-SQLAlchemy, Flask-Migrate |
| **Database**          | MySQL                                          |
| **Server**            | Gunicorn / uWSGI                               |
| **Development Tools** | VS Code, Git, MySQL Workbench                  |


### 6. Functional Modules

#### Account Management

* User registration and login
* Admin-level user management (add, delete, query users)
* Secure authentication and password handling

####  Typhoon Information Management

* Add, edit, delete, and query typhoon records
* Filter by ID, region, or intensity
* Manage typhoon metadata and track updates

#### Notification & Subscription

* Users subscribe to specific typhoons
* Admin publishes important alerts or news
* Real-time notifications displayed to subscribers

#### Visualization & Analytics

* Display typhoon paths on an interactive map
* Show real-time tracking data and intensity levels


### 7. Setup & Deployment

#### Prerequisites

* Python 3.9+
* MySQL 8.0+
* Flask and dependencies


### 8. License

This project is released under the **MIT License**.
You are free to use, modify, and distribute it for educational or research purposes.

