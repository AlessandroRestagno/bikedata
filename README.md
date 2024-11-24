
# **My Dash App**

Welcome to **My Dash App**, a web application for uploading and analyzing `.FIT` files. This app allows users to visualize and understand their cycling data interactively.

---

## **Features**
- Upload `.FIT` files directly through the app.
- Parse and analyze cycling data such as power zones, timestamps, and other metrics.
- Visualize time spent in power zones using interactive charts.
- Simple and user-friendly interface.

---

## **Installation**

### Prerequisites
- Python 3.8 or later
- `pip` (Python package manager)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/AlessandroRestagno/bikedata.git
   cd bikedata
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app locally:
   ```bash
   python app.py
   ```

5. Open the app in your browser:
   ```
   http://127.0.0.1:8050/
   ```

---

## **File Upload**

1. Drag and drop or select a `.FIT` file on the upload box.
2. The app will analyze the file and display results, including:
   - Power zone distribution
   - Time spent in each zone
   - Additional metrics based on the uploaded data

---

## **Deployment**

This app is deployed on Heroku. To deploy:

1. Install the Heroku CLI:
   ```bash
   https://devcenter.heroku.com/articles/heroku-cli
   ```

2. Log in to Heroku:
   ```bash
   heroku login
   ```

3. Create a Heroku app:
   ```bash
   heroku create <app-name>
   ```

4. Push to Heroku:
   ```bash
   git push heroku main
   ```

5. Visit your deployed app:
   ```
   https://<app-name>.herokuapp.com/
   ```

---

## **Project Structure**
```
my_dash_app/
├── assets/               # Static assets (CSS, JS, images)
│   ├── styles.css
├── app.py                # Main Dash app file
├── callbacks.py          # Callbacks for interactivity
├── layouts.py            # App layout definition
├── data_processing.py    # Helper functions for data parsing
├── requirements.txt      # Dependencies
├── Procfile              # Heroku configuration
├── runtime.txt           # Python version for Heroku
└── README.md             # Project documentation
```

---

## **Dependencies**

This app uses the following Python libraries:
- [Dash](https://dash.plotly.com/) - Web framework for building interactive apps
- [Plotly](https://plotly.com/python/) - Interactive plotting library
- [Pandas](https://pandas.pydata.org/) - Data analysis and manipulation
- [fitparse](https://github.com/dtcooper/python-fitparse) - Library for parsing `.FIT` files
- [Gunicorn](https://gunicorn.org/) - WSGI HTTP Server for deployment

To install all dependencies:
```bash
pip install -r requirements.txt
```

---

## **Screenshots**
![Screenshot 1](assets/screenshot1.png)
*Example of the file upload interface.*

![Screenshot 2](assets/screenshot2.png)
*Visualization of time spent in power zones.*

---

## **Contributing**

Feel free to contribute to this project! Open issues, submit pull requests, or suggest new features. 

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**

- Inspired by cyclists and developers passionate about data and fitness!
- Built with ❤️ using [Dash](https://dash.plotly.com/) and Python.
