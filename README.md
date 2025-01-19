SOLUTION FOR EFFECTIVE UTILIZATION OF COIR RAW MATERIAL TO AVOID WASTAGE

Description

This project is a web application designed to optimize the utilization of coir raw material by creating an interactive platform for farmers, industries, and data analysts. The website provides tailored functionalities for each type of user:

User Roles and Pages:

1. Farmer Login:

   - Registration and Login.

   - Access to Farmer Dashboard, Industry Offers, Request Form, Transaction Details, Feedback, FAQs, and Logout.

2. Industry Login:

   - Registration and Login.

   - Access to Requirement Form, Farmer Requests, Transactions, Feedback, and Logout.

3. Data Analyst (DA) Login:

   - Registration and Login.

   - Access to Transactions, Feedback, and Logout.

Workflow:

   - Industry users submit requirements through a requirement form. The data is stored in the industryRequirement model.

   - Farmers review industry offers on the Farmer Page and send requests to industries by updating their availability, mobile number, and UPI ID through a request form. The data is stored in the farmerRequest model.

   - Industries can view farmer requests on the Industry Page. Upon accepting a request, a payment form is displayed for transaction completion.

   - Request statuses are updated and displayed on the Farmer Dashboard.

   - Transactions are recorded in the database and can be accessed by respective users. Data Analysts can view all transactions.

   - Users can send feedback to the admin, and farmers can use the FAQ section for navigation assistance.

   - Logout functionality is available for all users.

Technology Stack

Frontend:

 - HTML, CSS, JavaScript

Backend:

 - Django Framework

Database:

 - SQLite (default)

 - PostgreSQL/MySQL (optional)

User Authentication:

 - Django Authentication System

Version Control:

 - Git and GitHub

Features

 - Multi-User Support: Separate login and dashboard for Farmers, Industries, and Data Analysts.

 - Interactive Interfaces: Intuitive navigation and forms tailored to each user role.

 - Transaction Management: Secure recording and display of transactions for all stakeholders.

 - Feedback and Support: Feedback forms and an FAQ section for user assistance.

 - Scalability: Optional integration with PostgreSQL/MySQL for enhanced database performance.
