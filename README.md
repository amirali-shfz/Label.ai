# CS348-Project

# Required installations
- Node.js >= 14
- PSQL
- All packages inside `backend/requirements/base.txt`

### Postgresql on Mac

1. Open the terminal application on your mac.

2. Install Homebrew. This helps with installing and managing applications on MacOS. Simply run:

   ```bash
   /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
   ```

3. Update Homebrew and install postgresql by running:

   ```bash
   brew update
   brew install postgresql
   ```

4. Check to make sure you have PostgreSQL by checking its version:

   ```bash
   postgres --version
   # This must print something like:
   # > postgres (PostgreSQL) 12.2
   ```

5. Now you can initialize the physical space on your hard-disk to allocate databases. To do this, create a default *postgres* database on the command line. Run:

   ```bash
   initdb /usr/local/var/postgres
   # You will/might see "initdb: directory "/usr/local/var/postgres" exists but is not empty"
   # this means the database was already created and you are fine for this step
   ```

6. Start the database by running:

   ```bash
   pg_ctl -D /usr/local/var/postgres start
   ```

### The Website
1. Create a virtualenv:
   ```bash
   python3.9 -m venv <virtual env path>
   ```
2. Activate the virtualenv you have just created:

   ```bash
   source <virtual env path>/bin/activate
   ```
3. install requirements:
   ```bash
   pip install -r requirements/local.txt
   ```
4. Create a db:
   ```bash
   createdb label_ai -U postgres --password <password>
   ```
5. Set the environment variables for your database:
   ```bash
   export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/label_ai
   ```

6. Apply migrations:

   ```bash
   python manage.py migrate
   ```

7. Run the server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
8. Visist `0.0.0.0:8000` and enjoy! The 2 functionalities currently supported are:
   
   - List all images: `0.0.0.0:8000/images/` 
   - List all labels: `0.0.0.0:8000/labels/`

