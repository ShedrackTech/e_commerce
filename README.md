# 🛒 Django E-Commerce

A full-featured e-commerce web application built with Django, developed as part of the **6milian Coding Academy** tutorial series.

---

## ✨ Features

- 🛍️ Product catalogue with categories and filtering
- 🔍 Product search
- 🛒 Shopping cart (session-based)
- 💳 Order management and checkout
- 👤 Custom user authentication (register, login, logout)
- 🔐 Password change, reset, and recovery via email
- 📋 User profile with shipping address
- 📬 Contact form with admin inbox and reply system
- 🔑 Admin panel with full message management
- 🎨 Dark-themed modern UI
- 📱 Fully responsive (Bootstrap 4)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django 6 |
| Frontend | Bootstrap 4, HTML5, CSS3, JavaScript |
| Database | SQLite (development) |
| Forms | django-crispy-forms |
| Email | SMTP (Gmail) |
| Environment | python-dotenv |
| Version Control | Git & GitHub |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShedrackTech/e_commerce.git
   cd e_commerce
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your@gmail.com
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit the app**
   - Site: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
e_commerce/
├── shop/                  # Main app (products, auth, contact)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
├── cart/                  # Shopping cart app
├── order/                 # Order processing app
├── coupons/               # Discount coupons app
├── ecommerce/             # Project settings
│   ├── settings.py
│   └── urls.py
├── manage.py
├── .env                   # Environment variables (not committed)
├── .gitignore
└── requirements.txt
```

---

## 📬 Contact Form & Admin Inbox

Submitted contact messages are saved to the database and visible in the Django admin panel under **Shop → Contact Messages**. Admins can:

- View unread/read messages with status badges
- Reply directly from the admin panel (sends a real email)
- Filter by read status, reply status, and subject
- Bulk mark messages as read or unread

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for development, `False` for production |
| `EMAIL_HOST` | SMTP server (e.g. `smtp.gmail.com`) |
| `EMAIL_PORT` | SMTP port (usually `587`) |
| `EMAIL_HOST_USER` | Your email address |
| `EMAIL_HOST_PASSWORD` | App password (not your real password) |
| `EMAIL_USE_TLS` | `True` |
| `DEFAULT_FROM_EMAIL` | Sender email address |

---

## 📚 Tutorial Series

This project was built following the **6milian Coding Academy** Django e-commerce tutorial. It is intended for learning purposes and demonstrates real-world Django patterns including:

- Class-based and function-based views
- Custom user models
- Django admin customisation
- Form handling and validation
- Session-based cart management
- Email integration

---

## 👨‍💻 Author

**Shedrack Ugwu**
GitHub: [@ShedrackTech](https://github.com/ShedrackTech)

---

## 📄 License

This project is for educational purposes as part of the 6milian Coding Academy curriculum.
