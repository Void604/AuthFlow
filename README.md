# AuthFlow: Patient & Doctor User Authentication System

[![Google Drive – App Files & Demo Video](https://img.shields.io/badge/Google%20Drive-App%20Files%20%26%20Demo%20Video-blue?logo=google-drive)](https://drive.google.com/drive/u/1/folders/1rRzRuLzJg1rRHrEhlw6QjRsjaD3paVz1)
> **Access the complete application files and a demo video on Google Drive:**  
> [https://drive.google.com/drive/u/1/folders/1rRzRuLzJg1rRHrEhlw6QjRsjaD3paVz1](https://drive.google.com/drive/u/1/folders/1rRzRuLzJg1rRHrEhlw6QjRsjaD3paVz1)

AuthFlow is a simple web application built with Flask that allows users to sign up as either a **Patient** or a **Doctor**, log in, and then access their respective personalized dashboards displaying their registered details.

---

## ✨ Features

- **User Types:** Supports two distinct user roles: Patient and Doctor.
- **Secure Signup:**
  - Fields for First Name, Last Name, Profile Picture (URL), Username, Email, Password, Confirm Password, and Address (Line 1, City, State, Pincode).
  - Password and Confirm Password matching validation.
  - Basic email format validation.
  - Checks for unique usernames and email addresses.
- **User Login:** Allows users to log in using their username or email and password.
- **Role-Based Dashboards:** Redirects logged-in users to either a Patient Dashboard or a Doctor Dashboard based on their registered type.
- **User-Friendly Interface:** Built with HTML and styled using Tailwind CSS for a modern and responsive design.
- **Session Management:** Maintains user login status using Flask sessions.
- **Flash Messages:** Provides interactive feedback to the user for success, errors, and informational messages.

---

## 🚀 Technologies Used

- **Backend:** Python 3
- **Web Framework:** Flask
- **Database:** SQLite3 (built-in Python database)
- **Password Hashing:** `bcrypt` Python library
- **Templating Engine:** Jinja2 (used by Flask for HTML rendering)

**Frontend:**
- HTML5
- CSS3
- Tailwind CSS (for rapid, utility-first styling)

---

## 📁 Project Structure

```
UserAuthApp/
├── app.py                      # Main Flask application logic
├── users.db                    # SQLite database file (created automatically on first run)
├── templates/                  # Contains all HTML template files
│   ├── base.html               # Base template for consistent layout
│   ├── signup.html             # Signup form
│   ├── login.html              # Login form
│   ├── patient_dashboard.html  # Patient's personalized dashboard
│   └── doctor_dashboard.html   # Doctor's personalized dashboard
└── static/                     # Contains static assets like CSS
    └── style.css               # Custom CSS styles (mostly Tailwind is used)
```

---

## 🛠️ Setup & Installation

Follow these steps to get the application up and running on your local machine.

### **Prerequisites**

- Python 3.x installed on your system.
- VS Code (recommended IDE)

### 1. **Clone the Repository (or create the project structure)**

If you're creating the project from scratch, ensure your folder structure matches the one described in "Project Structure" above.

If you were to clone, you would do:

```bash
git clone https://github.com/your-username/AuthFlow.git   # Replace with your repo URL
cd AuthFlow
```

For your case, you already have the files, just ensure they are in the `UserAuthApp` directory as described.

### 2. **Set up a Virtual Environment (Recommended)**

It's good practice to use a virtual environment to manage project dependencies.

```bash
# Navigate to your project directory if not already there
cd UserAuthApp

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. **Install Dependencies**

With your virtual environment activated, install the required Python libraries:

```bash
pip install Flask bcrypt
```

### 4. **Create Database Tables**

The `app.py` script automatically creates the `users.db` file and the necessary `users` table when the application starts for the first time.

---

## 🚀 How to Run

1. **Ensure your virtual environment is activated.**
2. **Navigate to the `UserAuthApp` directory in your terminal.**
3. **Run the Flask application:**

    ```bash
    python app.py
    ```

4. **Access the Application:**

   Open your web browser and go to the address displayed in your terminal, typically:
   ```
   http://127.0.0.1:5000/
   ```

---

## 👨‍💻 Usage

- **Sign Up:** On the initial page, you'll be presented with the signup form. Fill in your details, select "Patient" or "Doctor" as your account type, and click "Create Account".
- **Log In:** After successful signup, you'll be redirected to the login page. Enter your username/email and password.
- **Dashboard:** Upon successful login, you'll be taken to your respective dashboard (Patient or Doctor) where your registered details will be displayed.
- **Logout:** Use the "Logout" link in the header to end your session.

---

## 💡 Future Enhancements

- **Profile Editing:** Allow users to update their personal information.
- **Password Reset:** Implement a "Forgot Password" feature.
- **Image Upload:** Instead of just a URL, allow users to upload profile pictures directly.
- **Advanced Dashboards:** Add more specific functionalities and data displays for Patient and Doctor roles (e.g., appointment scheduling, patient list, medical records).
- **Form Validation (Client-Side):** Add JavaScript for instant feedback on form inputs before submission.
- **Improved Error Handling:** More user-friendly error pages.
- **Deployment:** Instructions for deploying the application to a live server (e.g., Heroku, AWS, DigitalOcean).

---

Feel free to contribute or suggest improvements!

  ## 👤 Author

* Aryan Kashyap
* aryankashyap7899@gmail.com
* [My Github Profile](https://github.com/Void604)
