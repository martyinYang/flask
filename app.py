from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/pet")
def pet():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("contact.html")

@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/update")
def update():
    return render_template("update.html")

if __name__ == "__main__":
    app.run()
