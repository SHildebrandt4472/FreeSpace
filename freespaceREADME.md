
![Logo](https://github.com/SHildebrandt4472/FreeSpace/blob/main/logo.png?raw=true)

# Freespace – Makerspace Management System

Freespace is a web-based application designed to help schools manage student access to specialized machinery and equipment in their technology and workshop spaces. It provides a structured system where students can request supervised bookings or apply for licenses to use tools independently. Teachers and platform managers have full control over machine configurations and booking approvals, making it easier to support student projects outside of regular class time.



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

7. Initialize the database with some data

```bash
   flask cli init_data
```

8. Start the app

```bash
   flask run
```

9. Open a browser and navigate to http://127.0.0.1:5000

10. Login with the following credentials<br>

    Use these credential for demo use as a <b>ADMIN</b> user:<br>
    username: Admin<br>
    password: Admin_password<br>

    Use these credentials for demo use as a <b>STUDENT</b> user:<br>
    username: Student<br>
    password: Student_password<br>

    To sign up as new users, click on the "Sign Up" button and use the registration codes:<br>
    For student = IAMASTUDENT<br>
    For staff = TEACHERSRULE<br>

11. You can now use the app

12. To sign up as a new user, press the logout button
    and select sign up. Use the registration code <b>SIGNMEUP</b> and fill in your details.

13. To stop the app, press Ctrl+C in the terminal


## How to Use

Freespace is designed with three main user roles: Students, Teachers, and Platform Managers (Admins). Each role has access to features tailored to their responsibilities and permissions within the system.

### Students:

- View all available workspaces and machines listed on the platform.

- Request booking slots for specific machines or workspaces

- Apply for skills/licenses related to specific machines. Once a student earns a skill, they can:

    - Book that machine independently, without requiring teacher approval.

    - Demonstrate their competence and safety awareness through practical or theoretical assessments.

This empowers students to take greater ownership of their learning while ensuring safety and proper use of tools.

### Teachers:

- Like students, they can view, book, and access all machines and workspaces.

- However, teachers are automatically equipped with all skills/licenses, meaning:

    - They do not need to apply for approval before booking any equipment.

    - They can directly reserve slots without supervision requirements.

- Teachers can also approve or deny student license requests and supervise sessions when needed.

### Workshop Managers, administrators can:

Admins are responsible for the overall management of the system and have access to full administrative functionality. They can:

- Create, configure, and manage all workspaces and machines on the platform.

    - Add and schedule available time slots for each workspace to determine when machines can be booked.

    - Manage users, including assigning roles and monitoring license progress.

    - Approve or reject student booking requests that require administrative approval.

    - Create and assign skills/licenses, ensuring that access to machines aligns with safety and training protocols.

Admins ensure that the makerspace remains well-organized, safe, and available to the school community in a structured way.


## License Information

This project is licensed under the [Mozilla Public License 2.0](https://github.com/SHildebrandt4472/FreeSpace/blob/main/LICENSE) . This License allows the use, ability to modify, and distribute the code freely, as long as any changes to MPL-licensed files are shared under the same license.


## Acknowledgements

- Inspired by makerspace models at UNSW and UTS
- Appreciation to educators who provided early feedback
- St Augustine's College for supporting this project, providing test data and resources to develop and test the application

## Author Details

This project was made and is maintained by Sam Hildebrandt as Software major work project of the Software Engineering course at St Augustines College.<br>
**Created by:** Sam Hildebrandt  
**Email:** shildebrandt@student.saintaug.nsw.edu.au.com  


## Documentation

Detailed documentation including program logic diagrams, detailed logs of development and information all about the application can be found in the documentation file:  
[FreeSpace Documentation](https://github.com/SHildebrandt4472/Task-Master/blob/main/freespace_documentation.pdf)