import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from summarizer import summarize_text
from storage import save_note, list_notes, get_note, delete_note, search_notes

app = typer.Typer()
console = Console()

# Create a separate Typer instance for the summarize subcommand
summarize_cli = typer.Typer()
app.add_typer(summarize_cli, name="summarize")

# Define the 'run' command under the 'summarize' subcommand
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

# Define the 'list' command to list all saved summaries
@app.command()
def list():
    """List all saved summaries."""
    from storage import list_notes
    notes = list_notes()
    for note in notes:
        console.print(f"[bold]{note['title']}[/bold]")
        console.print(f"Summary: {note['summary']}\n")

# Define the 'view' command to view a specific saved summary
@app.command()
def view(title: str):
    """View a saved note by title."""
    note = get_note(title)
    if not note:
        console.print(f"[red]Note '{title}' not found.[/red]")
        return
    console.print(f"\n[bold]{note['title']}[/bold] ({note['timestamp']})")
    console.print(f"\n[green]Summary:[/green]\n{note['summary']}")

# Define the 'delete' command to delete a saved summary
@app.command()
def delete(title: str):
    """Delete a saved note by title."""
    from storage import delete_note
    delete_note(title)

# Define the 'search' command to search notes by keyword
@app.command()
def search(keyword: str):
    """Search notes by keyword in title or summary."""
    results = search_notes(keyword)
    if not results:
        console.print(f"[yellow]No notes found matching '{keyword}'.[/yellow]")
        return
    table = Table(title=f"Search results for '{keyword}'")
    table.add_column("Title", style="bold cyan")
    table.add_column("Snippet", style="dim")
    for note in results:
        snippet = note["summary"][:60] + "..." if len(note["summary"]) > 60 else note["summary"]
        table.add_row(note["title"], snippet)
    console.print(table)

if __name__ == "__main__":
    app()