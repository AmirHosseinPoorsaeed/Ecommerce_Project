<h3>
    Ecommerce features
</h3>

<ul>
    <li>
        Advance admin panel
    </li>
    <li>
        Multilanguage
    </li>
    <li>
        Advance category system
    </li>
    <li>
        Filtering
    </li>
    <li>
        Searching system
    </li>
    <li>
        Choosing the time to send the shipment
    </li>
    <li>
        Discount system
    </li>
    <li>
        Advance comment system
    </li>
    <li>
        Session based cart
    </li>
    <li>
        Social registration
    </li>
</ul>

<hr>

<h3>
    ⚙️ Config the project
</h3>

<p>
    First you should make venv for this project. So in the main root of project you should type this command in your Terminal or Console:
</p>

<pre>
    python -m venv venv
</pre>

<p>
    Now you should activate your venv. So in the main root of project you shuold type this command in your Terminal or Console:
</p>

<b>
    In Linux/macOS:
</b>

<pre>
    source venv/bin/activate
</pre>

<b>
    In Windows:
</b>

<pre>
    venv/Scripts/activate
</pre>

<p>
    After activating venv you should install the <b>requirements.txt</b> packages. So type this command in your Terminal or Console: 
</p>

<pre>
    pip install -r requirements.txt
</pre>

<p>
    Then you need to create a database for this project and put the database information in the .env file
</p>



```python
  # .env file
  POSTGRES_USER=database_user
  POSTGRES_DB=database_name
  POSTGRES_PASSWORD=database_password
  POSTGRES_ENGINE=django.db.backends.postgresql
  POSTGRES_PORT=database_port
```

<p>
    After creating .env file and put the database information you need obtain OAuth2 credentials from <a href="https://console.developers.google.com/">google Developer Concole</a>
</p>

```python
  # .env file
  ...

  CLIENT_ID=...
  CLIENT_SECRET=...
```

<h5>
    Configuration of project almost done.
</h5>

<h3>
    🏁 Run the project
</h3>

<p>
    First of all, please enter the following command in the Terminal or Console to make sure the project is configured correctly:
</p>

<pre>
    python manage.py check
</pre>
<p>
    You should see This message:
        <strong>
            <i>
                "System check identified no issues (0 silenced)."
            </i>
        </strong>
    <br>
    If you see this message you should create your project database. So type this commands in Terminal or Console:
</p>

<pre>
    python manage.py makemigrations
</pre>

<pre>
    python manage.py migrate
</pre>

<p>
    After creating the project database, you should run project. So type this command in Terminal or Console:
</p>

<pre>
    python manage.py runserver
</pre>

<h4>
    Congratulations, you ran the project correctly ✅
</h4>


<p>
    Now copy/paste this address in your browser URL bar:
</p>

<pre>
    http://127.0.0.1:8000/
</pre>

<hr>

<h3>
    ✅ Use the project
</h3>

<p>
    For use the project first you should create a superuser. So type this command in Terminal or Console:
</p>

<pre>
    python manage.py createsuperuser
</pre>

<p>
    After creating a superuser you can login into your admin panels.
</p>

<pre>
    http://127.0.0.1:8000/admin/
</pre>