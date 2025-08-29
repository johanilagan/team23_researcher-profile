from researchd import create_app

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        print("Templates Flask can see:", app.jinja_loader.list_templates())
    app.run(debug=True)
