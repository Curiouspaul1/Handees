from . import client


@client.route("/")
def index():
    return "Hello!"