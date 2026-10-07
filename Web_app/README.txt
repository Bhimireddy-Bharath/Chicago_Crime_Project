Simple Flask + REST API + SQLite dashboard.

Copy app.py and templates/index.html into your existing Web_app folder.
Expected project structure:
Project_bharath/
  database/chicago_crime.db
  Graphs/*.png
  Web_app/app.py
  Web_app/templates/index.html

Run:
python app.py

Open:
http://127.0.0.1:5000

REST API:
GET    /api/status
GET    /api/crimes
GET    /api/crimes/<id>
POST   /api/crimes
PUT    /api/crimes/<id>
DELETE /api/crimes/<id>
