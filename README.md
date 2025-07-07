
![Logo](https://github.com/SHildebrandt4472/FreeSpace/blob/main/logo.png?raw=true)

# <img src = "https://github.com/SHildebrandt4472/FreeSpace/blob/main/app/static/icons/logo.svg" height = 25px> Freespace – Makerspace Management System

Freespace is a web-based application designed to help schools manage student access to specialized machinery and equipment in their technology and workshop spaces. It provides a structured system where students can request supervised bookings or apply for licenses to use tools independently. Teachers and platform managers have full control over machine configurations and booking approvals, making it easier to support student projects outside of regular class time.

## Features

- Unlimited workspaces
- Unlimited users
- Custom booking times per workspace
- Multiple user roles, Student, Teacher, Workshop Manager, Administrator
- Skills qualification management (users must have appropriate skills to make bookings for workspaces)
- Secure storage of personal details

## Screenshots

* Booking table with booked and available time slots
![Image 1](https://github.com/SHildebrandt4472/FreeSpace/blob/main/Screenshots/readme_1.png)

* User roles/management
![Image 6](https://github.com/SHildebrandt4472/FreeSpace/blob/main/Screenshots/readme_6.png)

* Dashboard page
![Image 2](https://github.com/SHildebrandt4472/FreeSpace/blob/main/Screenshots/readme_2.png)

* Booking approvals
![Image 3](https://github.com/SHildebrandt4472/FreeSpace/blob/main/Screenshots/readme_3.png)

* Skills/qualifications management
![Image 4](https://github.com/SHildebrandt4472/FreeSpace/blob/main/Screenshots/readme_4.png)


## Installation

1. Clone the git repository to a local directory

2. Change to the project directory

3. Create a virtual python environment in the project directory

```bash
   python -m venv venv
```

4. Activate the virtual environment
  (for WINDOWS)

```bash
   venv\Scripts\activate
```

5. Install the required packages

```bash
   pip install -r requirements.txt
```

6. Create the database

```bash  
   flask db upgrade
```

7. Initialize the database with some demonstration data

```bash
   flask cli init_demo
```

8. Start the app

```bash
   flask run
```

9. Open a browser and navigate to http://127.0.0.1:5000

10. Login with the following appropriate credentials credentials<br>

    Note: Demo data includes multiple users, each users password is the their username. The admin username is Sam with credentials:<br>
    Username: sam<br>
    Password: sam<br>
    Therefore after logging in as Sam, you can view all users and hence log in as other users which use the same credentials scheme with the password matching their username to test out individualised user features

    To sign up as new users, click on the "Sign Up" button and use the registration codes:<br>
    For student = IAMASTUDENT<br>
    For staff = TEACHERSRULE<br>

12. You can now use the app

13. To sign up as a new user, press the logout button
    and select sign up. Use the appropriate registration codes and fill in your details.

14. To stop the app, press Ctrl+C in the terminal

## User Guide

Freespace is designed with four main user roles: Students, Teachers, and Workspace Managers and system Admins. Each role has access to features tailored to their responsibilities and permissions within the system.

### Students:

- View all available workspaces and machines listed on the platform.

- Request booking slots for specific machines or workspaces.

- Review/modify future bookings.

- View/modify profile and change password.

This empowers students to take greater ownership of their learning while ensuring safety and proper use of tools.

### Teachers:

- Like students, they can view, book, and access all machines and workspaces.

- They do not need to apply for approval after booking any equipment.


### Workshop Managers:

Workspace managers are responsible for the overall management of the workspaces and skills/qualifications system. They can:

- Create, configure, and manage all workspaces and machines on the platform.

    - Add and schedule available time slots for each workspace to determine when machines can be booked.

    - Approve or reject student booking requests that require administrative approval.

    - Create and assign skills/qualifications, ensuring that access to machines aligns with safety and training protocols.


### Admin

Admins ensure that the makerspace remains well-organized, safe, and available to the school community in a structured way. Admins have full privileges aswell as control over user management.


## License Information

This project is licensed under the [Mozilla Public License 2.0](https://github.com/SHildebrandt4472/FreeSpace/blob/main/LICENSE) . This License allows the use, ability to modify, and distribute the code freely, as long as any changes to MPL-licensed files are shared under the same license.


## Acknowledgements

- Inspired by makerspace booking platform models at UNSW and UTS
- St Augustine's College for supporting this project, providing test data and resources to develop and test the application

## Author Details

This project was made and is maintained by Sam Hildebrandt as a Software major work project of the Software Engineering course at St Augustines College.<br>
**Created by:** Sam Hildebrandt  
**Email:** shildebrandt@student.saintaug.nsw.edu.au.com  


## Documentation

Detailed documentation including program logic diagrams, detailed logs of development and information all about the application can be found in the documentation file:  
[FreeSpace Documentation](https://github.com/SHildebrandt4472/Task-Master/blob/main/freespace_documentation.pdf)
