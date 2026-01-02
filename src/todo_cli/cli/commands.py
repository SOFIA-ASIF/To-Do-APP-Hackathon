"""CLI commands for todo management."""
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn
from datetime import datetime
import time
import random
from todo_cli.services.todo_service import TodoService


# Initialize the service and console
todo_service = TodoService()
console = Console()

# Fun emoji collections
CELEBRATION_EMOJIS = ["🎉", "🎊", "🎈", "🌟", "✨", "🎆", "🎇", "💫", "⭐", "🌠"]
ANIMAL_EMOJIS = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵"]
FOOD_EMOJIS = ["🍕", "🍔", "🍟", "🌭", "🍿", "🧃", "🍦", "🍩", "🍪", "🎂", "🍰", "🧁", "🍬", "🍭"]
ACTIVITY_EMOJIS = ["⚽", "🏀", "🏈", "⚾", "🎾", "🏐", "🎮", "🎯", "🎨", "🎭", "🎪", "🎢", "🎡"]

def get_random_emoji(category="celebration"):
    """Get a random emoji from a category."""
    categories = {
        "celebration": CELEBRATION_EMOJIS,
        "animal": ANIMAL_EMOJIS,
        "food": FOOD_EMOJIS,
        "activity": ACTIVITY_EMOJIS
    }
    return random.choice(categories.get(category, CELEBRATION_EMOJIS))

def rainbow_text(text):
    """Create rainbow colored text."""
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    result = Text()
    for i, char in enumerate(text):
        result.append(char, style=colors[i % len(colors)])
    return result

def show_spinner_animation(message, duration=1.5):
    """Show a fun spinner animation."""
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold cyan]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(message, total=None)
        time.sleep(duration)


@click.group()
def cli():
    """🌈 Super Fun Todo List Manager! 🎮"""
    pass


@cli.command()
@click.argument('title', nargs=-1, required=True)
def add(title):
    """✨ Add a super cool new todo! ✨
    
    Example:
        todo add Play with my toys
        todo add "Do homework and get a gold star"
    """
    title_str = ' '.join(title)
    
    show_spinner_animation(f"Adding your awesome todo {get_random_emoji('celebration')}")
    
    try:
        new_todo = todo_service.add_todo(title_str)
        
        # Create a super fun success panel
        success_text = Text()
        celebration = "".join([get_random_emoji('celebration') for _ in range(5)])
        
        success_text.append(f"{celebration}\n", style="bold")
        success_text.append("WOOHOO! TODO ADDED!\n", style="bold yellow on blue")
        success_text.append(f"{celebration}\n\n", style="bold")
        
        success_text.append("📝 Your Mission: ", style="bold magenta")
        success_text.append(f"{new_todo.title}\n\n", style="bold white")
        
        success_text.append("🎯 Mission ID: ", style="bold cyan")
        success_text.append(f"{new_todo.id}\n\n", style="dim yellow")
        
        success_text.append(f"{get_random_emoji('animal')} ", style="")
        success_text.append("You're doing GREAT! Keep it up, superstar!", style="bold green")
        
        console.print(Panel(
            success_text, 
            border_style="bold yellow",
            box=box.DOUBLE,
            style="on #5F9598"
        ))
        
    except ValueError as e:
        console.print(Panel(
            f"[bold red]😢 Oopsie! {str(e)}[/bold red]",
            title="[bold]Uh Oh![/bold]",
            border_style="red",
            box=box.HEAVY
        ))
        raise click.Abort()


@cli.command()
@click.option('--all', '-a', 'show_all', is_flag=True, help='Show all todos including completed')
@click.option('--completed', '-c', 'show_completed', is_flag=True, help='Show only completed todos')
def list(show_all, show_completed):
    """🎨 See all your awesome missions! 🎨
    
    Example:
        todo list
        todo list --all
        todo list --completed
    """
    show_spinner_animation(f"Loading your missions {get_random_emoji('activity')}")
    
    todos = todo_service.get_all_todos()
    
    if not todos:
        empty_message = Text()
        empty_message.append("🎈 ", style="bold yellow")
        empty_message.append("No missions yet!\n\n", style="bold cyan")
        empty_message.append(f"{get_random_emoji('animal')} ", style="")
        empty_message.append("Start by adding something fun to do!\n", style="white")
        empty_message.append("Type: ", style="dim")
        empty_message.append("todo add <something fun>", style="bold magenta")
        
        console.print(Panel(
            empty_message,
            title=rainbow_text("🌟 Mission Control 🌟"),
            border_style="yellow",
            box=box.DOUBLE
        ))
        return
    
    # Filter todos based on flags
    if show_completed:
        todos = [todo for todo in todos if todo.completed]
        title_text = "⭐ COMPLETED MISSIONS ⭐"
        border_color = "green"
        emoji_theme = "celebration"
    elif not show_all:
        todos = [todo for todo in todos if not todo.completed]
        title_text = "🎯 ACTIVE MISSIONS 🎯"
        border_color = "cyan"
        emoji_theme = "activity"
    else:
        title_text = "🌈 ALL YOUR MISSIONS 🌈"
        border_color = "magenta"
        emoji_theme = "animal"
    
    if not todos:
        if show_completed:
            message = f"[green]{get_random_emoji('celebration')} No completed missions yet! You got this![/green]"
        else:
            message = f"[green]{get_random_emoji('celebration')} All done! You're a SUPERSTAR! Use --all to see everything![/green]"
        
        console.print(Panel(
            message,
            title=rainbow_text(title_text),
            border_style=border_color,
            box=box.DOUBLE
        ))
        return
    
    # Create a super colorful table
    table = Table(
        show_header=True,
        header_style="bold white on blue",
        border_style=f"bold {border_color}",
        box=box.DOUBLE_EDGE,
        title=rainbow_text(title_text),
        show_lines=True,
        padding=(0, 1)
    )
    
    table.add_column("🎯", style="bold", width=4, justify="center")
    table.add_column("Status", justify="center", width=12)
    table.add_column("Your Mission", style="bold white", min_width=30)
    table.add_column("Mission Code", style="dim cyan", width=36)
    table.add_column("Created", style="dim yellow", width=19)
    
    for idx, todo in enumerate(todos, 1):
        if todo.completed:
            status = f"[green]✅ DONE![/green]"
            title_style = "bold green"
            mission_text = f"{get_random_emoji('celebration')} {todo.title}"
        else:
            status = f"[yellow]⏳ TODO[/yellow]"
            title_style = "bold cyan"
            mission_text = f"{get_random_emoji(emoji_theme)} {todo.title}"
        
        created_date = todo.created_at.strftime('%Y-%m-%d %H:%M')
        
        # Alternate row colors for fun
        row_style = "on rgb(40,0,40)" if idx % 2 == 0 else "on rgb(0,40,40)"
        
        table.add_row(
            str(idx),
            status,
            Text(mission_text, style=title_style),
            todo.id,
            created_date,
            style=row_style
        )
    
    console.print()
    console.print(table)
    console.print()
    
    # Add fun footer messages
    if not show_all and not show_completed:
        footer = Text()
        footer.append(f"{get_random_emoji('animal')} ", style="")
        footer.append("Pro Tip: ", style="bold yellow")
        footer.append("Use ", style="dim")
        footer.append("--all", style="bold magenta")
        footer.append(" to see everything or ", style="dim")
        footer.append("--completed", style="bold green")
        footer.append(" to see your victories!", style="dim")
        console.print(footer)
        console.print()


@cli.command()
@click.argument('todo_id')
def complete(todo_id):
    """🎉 Mark a mission as COMPLETE! 🎉
    
    Example:
        todo complete <mission-id>
    """
    show_spinner_animation(f"Completing mission {get_random_emoji('celebration')}")
    
    updated_todo = todo_service.complete_todo(todo_id)
    
    if updated_todo:
        # Super celebration!
        celebration = "".join([get_random_emoji('celebration') for _ in range(8)])
        
        success_text = Text()
        success_text.append(f"\n{celebration}\n", style="bold")
        success_text.append("🏆 MISSION ACCOMPLISHED! 🏆\n", style="bold yellow on green")
        success_text.append(f"{celebration}\n\n", style="bold")
        
        success_text.append("You completed: ", style="bold cyan")
        success_text.append(f"{updated_todo.title}\n\n", style="bold white")
        
        congrats_messages = [
            "You're AMAZING! 🌟",
            "AWESOME JOB! 💪",
            "Super cool! 🎨",
            "You rock! 🎸",
            "Fantastic work! 🎭",
            "You're a STAR! ⭐",
            "Brilliant! 💎",
            "WOW! Just WOW! 🤩"
        ]
        
        success_text.append(f"\n{random.choice(congrats_messages)}", style="bold magenta")
        
        console.print(Panel(
            success_text,
            border_style="bold green",
            box=box.DOUBLE,
            style="on blue"
        ))
    else:
        console.print(Panel(
            f"[bold red]😢 Oopsie! Can't find mission: {todo_id}[/bold red]\n\n"
            f"[dim]Try[/dim] [bold cyan]todo list[/bold cyan] [dim]to see your missions![/dim]",
            title="[bold red]Mission Not Found![/bold red]",
            border_style="red",
            box=box.HEAVY
        ))
        raise click.Abort()


@cli.command()
@click.argument('todo_id')
@click.argument('new_title', nargs=-1, required=True)
def update(todo_id, new_title):
    """✏️ Change your mission details! ✏️
    
    Example:
        todo update <mission-id> New super fun title
    """
    new_title_str = ' '.join(new_title)
    
    show_spinner_animation(f"Updating mission {get_random_emoji('activity')}")
    
    try:
        updated_todo = todo_service.update_todo_title(todo_id, new_title_str)
        
        if updated_todo:
            success_text = Text()
            success_text.append("✨✏️✨\n", style="bold yellow")
            success_text.append("MISSION UPDATED!\n", style="bold cyan on magenta")
            success_text.append("✨✏️✨\n\n", style="bold yellow")
            
            success_text.append("New Mission: ", style="bold magenta")
            success_text.append(f"{updated_todo.title}\n\n", style="bold white")
            
            success_text.append(f"{get_random_emoji('animal')} Great choice! Let's do this!", style="bold green")
            
            console.print(Panel(
                success_text,
                border_style="bold blue",
                box=box.DOUBLE
            ))
        else:
            console.print(Panel(
                f"[bold red]😢 Can't find mission: {todo_id}[/bold red]",
                title="[bold]Oopsie![/bold]",
                border_style="red",
                box=box.HEAVY
            ))
            raise click.Abort()
    except ValueError as e:
        console.print(Panel(
            f"[bold red]😢 Oopsie! {str(e)}[/bold red]",
            border_style="red",
            box=box.HEAVY
        ))
        raise click.Abort()


@cli.command()
@click.argument('todo_id')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
def delete(todo_id, force):
    """🗑️ Remove a mission! 🗑️
    
    Example:
        todo delete <mission-id>
        todo delete <mission-id> --force
    """
    todo = todo_service.get_todo_by_id(todo_id)
    
    if not todo:
        console.print(Panel(
            f"[bold red]😢 Can't find mission: {todo_id}[/bold red]",
            title="[bold]Mission Not Found![/bold]",
            border_style="red",
            box=box.HEAVY
        ))
        raise click.Abort()
    
    if not force:
        console.print()
        warning = Text()
        warning.append("⚠️  ", style="bold yellow")
        warning.append("Wait! Are you sure?\n\n", style="bold yellow")
        warning.append("You're about to delete:\n", style="white")
        warning.append(f"{todo.title}\n\n", style="bold cyan")
        warning.append("This can't be undone! ", style="dim red")
        warning.append(f"{get_random_emoji('animal')}", style="")
        
        console.print(Panel(
            warning,
            border_style="yellow",
            box=box.DOUBLE
        ))
        
        if not click.confirm('\n🤔 Really delete this mission?', default=False):
            console.print(f"\n[green]{get_random_emoji('celebration')} Phew! Mission saved![/green]\n")
            return
    
    show_spinner_animation("Deleting mission...")
    
    deleted = todo_service.delete_todo(todo_id)
    
    if deleted:
        console.print()
        delete_text = Text()
        delete_text.append("🗑️ ", style="bold")
        delete_text.append("Mission Deleted\n\n", style="bold red")
        delete_text.append(f"{todo.title}\n\n", style="dim white")
        delete_text.append("Don't worry, you can always add more missions! ", style="dim")
        delete_text.append(f"{get_random_emoji('animal')}", style="")
        
        console.print(Panel(
            delete_text,
            border_style="red",
            box=box.DOUBLE
        ))


@cli.command()
def stats():
    """📊 See your AWESOME stats! 📊
    
    Example:
        todo stats
    """
    show_spinner_animation(f"Calculating your awesomeness {get_random_emoji('celebration')}")
    
    todos = todo_service.get_all_todos()
    
    if not todos:
        console.print(Panel(
            f"[yellow]{get_random_emoji('animal')} No missions yet to analyze![/yellow]\n\n"
            f"[dim]Start with:[/dim] [bold cyan]todo add <something fun>[/bold cyan]",
            title=rainbow_text("📊 Stats Center 📊"),
            border_style="yellow",
            box=box.DOUBLE
        ))
        return
    
    total = len(todos)
    completed = sum(1 for todo in todos if todo.completed)
    active = total - completed
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    # Create super fun statistics table
    table = Table(
        show_header=False,
        border_style="bold magenta",
        box=box.DOUBLE_EDGE,
        title=rainbow_text("🎮 YOUR AWESOME STATS 🎮"),
        show_lines=True,
        style="on rgb(20,0,40)"
    )
    
    table.add_column("Metric", style="bold yellow", width=25)
    table.add_column("Score", style="bold white on blue", width=12, justify="center")
    table.add_column("Power Bar", style="", width=35)
    
    # Total todos
    bar_total = "".join([random.choice(["🟦", "🟨", "🟩", "🟪"]) for _ in range(min(total, 30))])
    table.add_row(
        "📝 Total Missions",
        f"✨ {total} ✨",
        bar_total
    )
    
    # Active todos
    bar_active = "🟨" * min(active, 30)
    table.add_row(
        "⏳ Active Missions",
        f"🎯 {active} 🎯",
        bar_active
    )
    
    # Completed todos
    bar_completed = "🟩" * min(completed, 30)
    table.add_row(
        "✅ Completed",
        f"🏆 {completed} 🏆",
        bar_completed
    )
    
    # Completion rate
    rate_blocks = int(completion_rate / 3.33)
    bar_rate = "⭐" * rate_blocks
    table.add_row(
        "📈 Completion Power",
        f"💪 {completion_rate:.0f}% 💪",
        bar_rate
    )
    
    console.print()
    console.print(table)
    console.print()
    
    # Super fun motivational messages
    if completion_rate == 100:
        message = Text()
        message.append("🎉🎊🎈 ", style="bold")
        message.append("PERFECT SCORE! ", style="bold green on yellow")
        message.append("🎈🎊🎉\n", style="bold")
        message.append("You're a SUPERHERO! ", style="bold magenta")
        message.append(f"{get_random_emoji('celebration')}", style="")
    elif completion_rate >= 70:
        message = Text()
        message.append(f"{get_random_emoji('celebration')} ", style="")
        message.append("AMAZING PROGRESS! ", style="bold cyan")
        message.append("You're doing SUPER! ", style="bold green")
        message.append(f"{get_random_emoji('animal')}", style="")
    elif completion_rate >= 40:
        message = Text()
        message.append(f"{get_random_emoji('activity')} ", style="")
        message.append("Keep going! ", style="bold yellow")
        message.append("You got this! ", style="bold cyan")
        message.append(f"{get_random_emoji('animal')}", style="")
    else:
        message = Text()
        message.append(f"{get_random_emoji('animal')} ", style="")
        message.append("Time for an adventure! ", style="bold magenta")
        message.append("Let's complete some missions! ", style="bold cyan")
        message.append(f"{get_random_emoji('celebration')}", style="")
    
    console.print(Panel(
        message,
        border_style="bold yellow",
        box=box.DOUBLE,
        style="on blue"
    ))
    console.print()

@cli.command()
def motivate():
    """🌟 Get a motivational boost! 🌟"""
    
    motivational_quotes = [
        ("You're AWESOME!", "bold yellow on blue", "celebration"),
        ("Keep being AMAZING!", "bold green on magenta", "animal"),
        ("You're a SUPERSTAR!", "bold cyan on red", "celebration"),
        ("YOU CAN DO IT!", "bold magenta on green", "activity"),
        ("Believe in yourself!", "bold yellow on purple", "celebration"),
        ("You're INCREDIBLE!", "bold green on blue", "animal"),
        ("Never give up!", "bold red on yellow", "activity"),
        ("YOU ROCK!", "bold blue on yellow", "celebration"),
    ]
    
    quote, style, emoji_cat = random.choice(motivational_quotes)
    
    show_spinner_animation("Generating motivation...")
    
    motivate_text = Text()
    emojis = "".join([get_random_emoji(emoji_cat) for _ in range(6)])
    
    motivate_text.append(f"{emojis}\n\n", style="bold")
    motivate_text.append(f"{quote}\n\n", style=style)
    motivate_text.append(f"{emojis}", style="bold")
    
    # Random border colors for variety
    border_colors = ["bold yellow", "bold magenta", "bold cyan", "bold green", "bold blue", "bold red"]
    
    console.print()
    console.print(Panel(
        motivate_text,
        title=rainbow_text("💪 MOTIVATION BOOST! 💪"),
        border_style=random.choice(border_colors),
        box=box.DOUBLE,
        padding=(2, 4)
    ))
    console.print()

if __name__ == '__main__':
    cli()