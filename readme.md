#Team Showface

##How to use

Copypaste the `square.py` file in `codeitsuisse/routes`
In `@app.route('/square', methods=['POST'])`, replace `/square` with the name of the endpoint specified in question
In `codeitsuisse/__init__.py`, add `import codeitsuisse.routes.yourfilename`
Then, in your shell:
```sh
git add .
git commit -m "Your message here"
git push origin master
git push heroku master
```
Run postman to run tests.
