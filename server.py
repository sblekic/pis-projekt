from website import create_app
app = create_app()

# pokreni server samo ako pokrenem main.py, tj server se nece pokrenuti ako npr
# importiram main u views.py i pokrenem views.py
if __name__ == "__main__":
    app.run(debug=True)
