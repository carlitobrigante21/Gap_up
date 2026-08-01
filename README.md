# GapUp - IT Career Path Simulator

GapUp is a lightweight, high-performance Server-Side Rendered (SSR) web application built to help aspiring IT professionals analyze skill gaps, calculate required learning hours, and visualize clear learning paths toward target technical roles.

---

## Tech Stack

* **Backend**: Python 3, Flask
* **Templating**: Jinja2 (SSR)
* **Database**: SQLite3
* **Styling**: Tailwind CSS (via CDN)

---

## Key Features

* **Dynamic Gap Analysis**: Compares a user's current skill set with the requirements of a target role.
* **Effort and Pace Estimation**: Calculates missing study hours and suggests realistic schedules for Casual, Moderate, and Intensive plans.
* **Automatic Database Setup**: Seeds and initializes the SQLite database when needed on first launch.
* **Structured Data Access**: Uses a dedicated database layer to keep role, skill, and certification data organized.

---

## How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Gap_up