from LibraryBookTracker import Book
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()
allBooks = []

while True:
    console.print("\n[bold cyan]📚 Library Manager[/bold cyan]")
    console.print("1. Add Book")
    console.print("2. Checkout Book")
    console.print("3. Return Book")
    console.print("4. List All Books")
    console.print("5. Exit")

    choice = Prompt.ask("[yellow]Choose[/yellow]", choices=["1", "2", "3", "4", "5"])

    if choice == "1":
        title = Prompt.ask("Title")
        author = Prompt.ask("Author")
        isbn = Prompt.ask("ISBN")
        allBooks.append(Book(title.strip(), author.strip(), isbn.strip()))
        console.print("[green]Book added![/green]")

    elif choice == "2":
        if not allBooks:
            console.print("[red]No books in library![/red]")
            continue
        isbn = Prompt.ask("Enter ISBN to checkout")
        for b in allBooks:
            if b.isbn == isbn:
                console.print(b.checkout())
                break
        else:
            console.print("[red]Book not found[/red]")

    elif choice == "3":
        if not allBooks:
            console.print("[red]No books in library![/red]")
            continue
        isbn = Prompt.ask("Enter ISBN to return")
        for b in allBooks:
            if b.isbn == isbn:
                console.print(b.return_book())
                break
        else:
            console.print("[red]Book not found[/red]")

    elif choice == "4":
        if not allBooks:
            console.print("[red]No books in library![/red]")
            continue
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Title")
        table.add_column("Author")
        table.add_column("ISBN")
        table.add_column("Status")
        for b in allBooks:
            status = "[green]Available[/green]" if b.is_available else "[red]Checked Out[/red]"
            table.add_row(b.title, b.author, b.isbn, status)
        console.print(table)

    elif choice == "5":
        console.print("[bold cyan]Bye![/bold cyan]")
        break
