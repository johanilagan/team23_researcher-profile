from researchd import create_app
from researchd.seed import seed

app = create_app()

app.cli.add_command(seed)

if __name__ == "__main__":
    with app.app_context():
        print("Templates Flask can see:", app.jinja_loader.list_templates())
    app.run(debug=True)