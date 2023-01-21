from anvolt.__init__ import __version__, __name__, __author__
from anvolt.request import HttpRequest
from tabulate import tabulate
import click


@click.group()
def main():
    pass


@main.command(help="Displays brief package information.")
def menu():
    text = f"""
    Author  : @{__author__}
    \nLicense : MIT
    \nGithub  : https://github.com/Stawa/anvolt.py
    \nAPI     : https://anvolt.vercel.app/api/
    """

    output = tabulate(
        [[text]],
        tablefmt="rounded_grid",
        headers=["{} - v{}".format(__name__, __version__)],
        numalign="center",
    )
    click.echo(output)


@main.command(help="Retrieves available categories with endpoint and method.")
def category_help():
    http_request = HttpRequest()
    click.echo(http_request.get(route="category"))


@main.command(help="Executes a test GET request to the specified endpoint.")
@click.option(
    "--category",
    "-c",
    help="Selects a category to retrieve the corresponding endpoint response.",
    required=True,
)
@click.option(
    "--endpoint",
    "-e",
    help="Retrieves endpoint response based on the previously selected category.",
    required=True,
)
def requests(category: str, endpoint: str):
    http_request = HttpRequest()
    response = http_request.get(route=f"{category.lower()}/{endpoint.lower()}")
    click.echo(response)
