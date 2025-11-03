import typer
from pathlib import Path
from rich.console import Console
from summarizer import summarize_text
from storage import save_note

app = typer.Typer()
console = Console()

# Create a separate Typer instance for the summarize subcommand
summarize_cli = typer.Typer()
app.add_typer(summarize_cli, name="summarize")


@summarize_cli.command(name="run")
def run(file: str):
    """Summarize a text file."""
    file_path = Path(file)
    if not file_path.exists():
        console.print(f"[bold red]Error:[/bold red] File '{file_path}' not found.")
        raise typer.Exit(code=1)

    text = file_path.read_text(encoding="utf-8")
    summary = summarize_text(text)

    console.print("\n[bold green]Summary:[/bold green]\n")
    console.print(summary)
    save_note(file_path.stem, text, summary)


if __name__ == "__main__":
    app()