# BriteCore Engineering

## Approch



## Deploy Manually
1. Create a new virtualenv
```bash
virtualenv -p python3.6 ENV
```
2. Activate the new virtual env.
```bash
source ENV/bin/activate
```
3. Clone this repo into your preferred working directory.
```bash
git clone https://github.com/codermeorg/briteEngine.git
```
4. Install the required python packages in requirements.txt
```bash
pip install -r requirements.txt
```
5. Create Database tables by running migrate
```bash
cd britecore
./manage.py migrate
```
6. Run the django-builtin HTTP server
```bash
./manage.py runserver
```


