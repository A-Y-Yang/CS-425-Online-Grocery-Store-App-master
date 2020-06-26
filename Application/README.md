Step 1: Download the repository

Step 2: Create a virtual environment

```python3 -m virtualenv venv```

Step 3: Activate the virtual environment

MacOS: ```source venv/bin/activate```

Windows: ```source venv\Scripts\activate```

Step 4: Install packages in the virtual environment

```pip install -r requirements.txt```

Step 5: Run run.py

```python run.py```

---
If you would like to setup the app in a new database, before Step 5, change line 11 in \_\_init\_\_.py

```app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://[username]:[password]@[host]/[database]'```

and then run run.py.

In the new database, you might run insertSampleData.py to insert the data in sample.sql to start. It will then be the same as the initital setup of our database.

```python insertSampleData.py```


