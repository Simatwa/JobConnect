from fastapi_cli.cli import app
import typer
from typing import Annotated
from api.fake_data import FakeJob, FakeUsers

jobconnect_app = typer.Typer(
    rich_markup_mode="rich", help="JobConnect utilities endpoint"
)

faker = typer.Typer(
    name="fake",
    help="Populate database models with [bold yellow]FAKE[/bold yellow] data",
)


@faker.command()
def job_category(
    amount: Annotated[
        int,
        typer.Option(
            help="Fake job [bold green]categories[/bold green] amount to be generated",
        ),
    ] = 50
):
    """Generate fake job categories"""
    fake_job = FakeJob()
    fake_job.category(amount)
    typer.secho(f"---{amount} job categories faked successfully---", fg="yellow")


@faker.command()
def jobs(
    amount: Annotated[
        int,
        typer.Option(
            help="Fake jobs amount to be generated",
        ),
    ] = 50
):
    """Generate fake [bold green]jobs[/bold green]"""
    fake_job = FakeJob()
    fake_job.job(amount)
    typer.secho(f"---{amount} jobs faked successfully---", fg="yellow")


@faker.command()
def users(
    amount: Annotated[
        int,
        typer.Option(
            help="Fake users amount to be generated",
        ),
    ] = 100
):
    """Generate fake [bold green]users[/bold green]"""
    fake_users = FakeUsers()
    fake_users.users(amount)
    typer.secho(f"---{amount} users faked successfully---", fg="yellow")


@faker.command()
def all(
    amount: Annotated[
        int,
        typer.Option(
            help="Fake entries amount to be made per model",
        ),
    ] = 20
):
    """Make entries into all db models with fake data"""
    FakeUsers().users(amount)
    typer.secho(f"---{amount} users faked successfully---", fg="yellow")
    fake_job = FakeJob()
    fake_job.category(amount)
    typer.secho(f"---{amount} job categories faked successfully---", fg="yellow")
    fake_job.job(amount)
    typer.secho(f"---{amount} jobs faked successfully---", fg="yellow")


jobconnect_app.add_typer(faker)

app.add_typer(jobconnect_app)

if __name__ == "__main__":
    app()
