# CS348-Project

# Required installations
- Node.js >= 14
- PSQL

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

### Postgresql on Windows

