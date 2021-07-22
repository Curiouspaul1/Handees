from core import create_app
import os

# create server instance from app factory
app = create_app(os.getenv("FLASK_CONFIG") or "default")


# configuring flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app
    )


if __name__ == "__main__":
    app.run()
