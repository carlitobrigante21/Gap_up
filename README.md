# GapUp - IT Career Path Simulator

GapUp is a lightweight, high-performance Server-Side Rendered (SSR) web application built to help aspiring IT professionals analyze skill gaps, calculate required learning hours, and visualize clear learning paths toward target technical roles.

---

## 🛠️ Tech Stack

* **Backend**: Python 3, Flask
* **Templating**: Jinja2 (SSR)
* **Database**: SQLite3
* **Styling**: Tailwind CSS (via CDN)

---

## 🚀 Key Features

* **Dynamic Gap Analysis**: Performs set-difference comparisons between a user's current skillset and target role requirements.
* **Effort & Pace Estimation**: Automatically calculates total missing hours and maps them to realistic study schedules (Casual, Moderate, Intensive).
* **Zero-Config Portability**: Automatically seeds and initializes the relational SQLite database on first launch if not present.
* **Modular Data Access**: Built with a clean separation of concerns using a dedicated Data Access Layer (`db.py`).

---

## 🏁 How to Run Locally

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Gap_up