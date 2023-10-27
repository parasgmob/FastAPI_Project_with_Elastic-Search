#Fastapi Social-app readme
Follow below steps for running social-app project successfully.

Create virtual environment using python3 -m venv env_name.

after creating virtual env use "source env_name/bin/activate" to active env.

After activating , install requirements.txt using pip install -r requirements.txt.

after installing all requirements change directory to project level using "cd app".

Now run "uvicorn main:app --reload" for running project locally.
you can also run on diffrent port using "uvicorn main:app --port port_number --reload".

After running successfully you can visit to openapi page of running project on "http://127.0.0.1:8000/docs".
You can also see docs of project using "http://127.0.0.1:8000/redoc"

You can stop running project "using Ctrl+C".

Or You Can simply run 'sudo docker-compose up' for starting project.
