# Label.ai

# Required installations
- Node.js >= 14
- PSQL
- All packages inside `backend/requirements/base.txt`
  - `python -m pip install backend/requirements/base.txt`

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

# The Website
1. Create a virtualenv:
   ```bash
   python3.9 -m venv venv
   ```
2. Activate the virtualenv you have just created:

   ```bash
   source venv/bin/activate
   ```
   
   ### Windows
   ```bash
   ./venv/Scripts/activate.bat
   ```
3. install requirements:
   ```bash
   pip install -r requirements/local.txt
   ```
4. Create a db:
   ```bash
   createdb label_ai -U postgres --password <password>
   ```
   
   ### Windows
   ```bash
   createdb -U postgres label_ai
   ```
5. Set the environment variables for your database:
   ```bash
   export DATABASE_URL=postgres://postgres:<password>@127.0.0.1:5432/label_ai
   ```
   ### Windows
   ```bash
   set DATABASE_URL=postgres://postgres@127.0.0.1:5432/label_ai
   ```
6. Apply migrations:

   ```bash
   python manage.py migrate
   ```

7. Run the server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
8. Visit `0.0.0.0:8000` and enjoy! The 2 functionalities currently supported are:
   
   - List all images: `0.0.0.0:8000/images/` 
   - List all labels: `0.0.0.0:8000/labels/`


# Features


`backend/label_ai/labels/views.py:`

1. List all labels

   lists all the labels in the Label table
   http://localhost:8000/labels/all

`backend/label_ai/classifications/views.py:`

2. List all classifications

   lists all the classifications in the Classification table
   http://localhost:8000//all

`backend/label_ai/members/views.py:`

3. List all members

   Lists all the members in the Member table
   http://localhost:8000/members/all

`backend/label_ai/submissions/views.py:`

4. List all submissions

   Lists all the submissions in the Submission table
   http://localhost:8000/submissions/all


5. Create Submission

   Creates a submission entry in the Submission table
   http://localhost:8000/submissions/insert (requires the fields of the submission object in the post call)

`queries/create_all.sql:`

6. Calculation of confidence for classifications (View + Joins)

   For each classification c, calculate the lower bound of the Wilson Confidence interval for ‘votes’ in submission corresponding to ‘c’, using user trust as a weighted vote.

   Confidence is represented in ClassificationView which is the endpoint for our application to make classification queries.

`backend/label_ai/images/views.py:`

7. List all images:

   Lists all the images in the Image table
   http://localhost:8000/images/all

8. ImagesByLabelView

   Returns a list of images by a label id. Will only return the images where the confidence / total count matches a certain threshold.
   http://localhost:8000/images/confirmed?label_id=<label_id>

9. MislabelledImagesView
   
   Queries all images we believe have one or more classifications with confidence < 0.05
   http://localhost:8000/images/mislabelled?count=<count>

10. GetPromptImageClassification

      Queries 1 random,unlabelled image classification prompt that
      http://localhost:8000/images/prompt


# Core Features


1. Get random classification prompts
Parameters for number of prompts and the user
User must not have classified previously
Prompts must be unconfirmed (actually need classification)

2. Get random classification prompts by label
Same 1. With label parameter

3. Submit a user classification - submission
Parameters for user, classification and their response
How to handle non-unique case? Triggers?

4. Get all images we are confident fall under a label

5. Get all the images with confident classification which were not previously classified

6. Get all the misclassified images which were previously classified

7. Calculate confidence in classifications
