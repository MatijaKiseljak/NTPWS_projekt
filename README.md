# Job Application Management System for Zagreb University of Applied Sciences
This project is a web-based system designed to facilitate job applications for various academic positions at Zagreb University of Applied Sciences. It was developed as part of a university course project.

## Features
- **User Management:**

  - Registration and login for applicants and administrators.
  - Role-based access to ensure secure and appropriate interactions.
- **Application Process:**

  - Support for multiple job positions including lecturer, senior lecturer, and professor roles.
  - Dynamic forms tailored to the requirements of specific job positions.
- **Administrative Panel:**

  - Review and manage job applications.
  - Filter, search, and sort applications for efficient handling.
- **File Uploads:**

  - Secure upload and storage of supporting documents such as diplomas, teaching materials, and research papers.
## Technology Stack
- **Backend**
  - The backend is built using the Django REST Framework, providing robust API endpoints to handle user authentication, application management, and data validation.

- **Frontend**
  - The frontend utilizes HTML and CSS, offering a user-friendly interface for both applicants and administrators.

## API Endpoints
- **Authentication**
  - POST `/register/`: Register a new user.
POST /login/: Login for applicants.
POST /admin-login/: Login for administrators.
POST /logout/: Logout.
- **Application Management**
GET /dashboard/: Dashboard for applicants.
POST /questionnaire/<position_id>/: Redirect to the specific questionnaire based on position ID.
POST /questionnaire/predavac-izbor/: Submit an application for "Predavač (izbor)".
POST /questionnaire/predavac-reizbor/: Submit an application for "Predavač (reizbor)".
POST /questionnaire/visipredavac-izbor/: Submit an application for "Viši predavač (izbor)".
POST /questionnaire/visipredavacre-izbor/: Submit an application for "Viši predavač (reizbor)".
POST /questionnaire/profesor-strucnog-studija-izbor/: Submit an application for "Profesor stručnog studija (izbor)".
POST /questionnaire/profesor-strucnog-studija-reizbor/: Submit an application for "Profesor stručnog studija (reizbor)".
POST /questionnaire/profesor-strucnog-studija-trajni/: Submit an application for "Profesor stručnog studija (trajni)".
- **Administration**
GET /admin-dashboard/: View and manage all applications.
GET /application/<id>/: View details of a specific application.
POST /application/<id>/delete/: Delete a specific application.
## Usage
- **For Applicants:**

Register and log in using the provided interface.
Select the desired position and complete the corresponding application form.
Upload required documents and submit the application.
- **For Administrators:**

Log in to access the administrative dashboard.
Review applications, filter by position, and manage submissions.
