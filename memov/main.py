import argparse
import logging
import os
import sys

from memov.core.manager import MemovManager

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for memov commands"""
    parser = argparse.ArgumentParser(
        description="memov - AI-assisted version control on top of Git", add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init
    init_parser = subparsers.add_parser("init", help="Initialize memov and git repository")
    init_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )

    # Track
    track_parser = subparsers.add_parser("track", help="Track files in the project directory")
    track_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )
    track_parser.add_argument(
        "file_paths", type=str, nargs="*", help="List of file path to track (optional, default: all files)"
    )
    track_parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default=None,
        required=False,
        help="Prompt for the tracked files (optional)",
    )
    track_parser.add_argument(
        "-r",
        "--response",
        type=str,
        default=None,
        required=False,
        help="Optional response for the tracked files",
    )
    track_parser.add_argument(
        "--by_user", "-u", action="store_true", help="Indicate that the files are tracked by the user"
    )

    # Snapshot
    snap_parser = subparsers.add_parser("snap", help="Create a snapshot with auto-generated ID")
    snap_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )
    snap_parser.add_argument(
        "-p", "--prompt", type=str, default=None, required=False, help="Prompt for the snapshot (required)"
    )
    snap_parser.add_argument(
        "-r", "--response", type=str, default=None, required=False, help="Optional response for the snapshot"
    )
    snap_parser.add_argument(
        "--by_user", "-u", action="store_true", help="Indicate that the snapshot is created by the user"
    )

    # Rename
    rename_parser = subparsers.add_parser("rename", help="Rename the files")
    rename_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )
    rename_parser.add_argument("old_path", type=str, help="Old path of the file (required)")
    rename_parser.add_argument("new_path", type=str, help="New path of the file (required)")
    rename_parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default=None,
        required=False,
        help="Prompt for the renamed files (optional)",
    )
    rename_parser.add_argument(
        "-r",
        "--response",
        type=str,
        default=None,
        required=False,
        help="Optional response for the renamed files",
    )
    rename_parser.add_argument(
        "--by_user", "-u", action="store_true", help="Indicate that the files are renamed by the user"
    )

    # Remove
    remove_parser = subparsers.add_parser("remove", help="Remove the files")
    remove_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )
    remove_parser.add_argument("file_path", type=str, help="Path of the file to remove (required)")
    remove_parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default=None,
        required=False,
        help="Prompt for the removed files (optional)",
    )
    remove_parser.add_argument(
        "-r",
        "--response",
        type=str,
        default=None,
        required=False,
        help="Optional response for the removed files",
    )
    remove_parser.add_argument(
        "--by_user", "-u", action="store_true", help="Indicate that the files are removed by the user"
    )

    # History
    history_parser = subparsers.add_parser("history", help="Show history of snapshots")
    history_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )

    # Show
    show_parser = subparsers.add_parser("show", help="Show details of a specific snapshot")
    show_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )
    show_parser.add_argument("prompt_id", type=str, help="ID of the snapshot to show")

    # Jump
    jump_parser = subparsers.add_parser("jump", help="Jump to a specific snapshot")
    jump_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )
    jump_parser.add_argument("prompt_id", type=str, help="ID of the snapshot to jump to")

    # Status
    status_parser = subparsers.add_parser(
        "status", help="Show status of working directory compared to latest snapshot"
    )
    status_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )

    # Amend
    amend_parser = subparsers.add_parser("amend", help="Amend a commit's message with prompt/response")
    amend_parser.add_argument(
        "--loc", type=str, default=".", help="Specify the project directory path (default: current directory)"
    )
    amend_parser.add_argument("commit_hash", type=str, help="Commit hash to amend (required)")
    amend_parser.add_argument("-p", "--prompt", type=str, default=None, help="Prompt to add (optional)")
    amend_parser.add_argument("-r", "--response", type=str, default=None, help="Response to add (optional)")
    amend_parser.add_argument(
        "-u", "--by_user", action="store_true", help="Indicate the source is user (default: AI)"
    )

    subparsers = {
        "init": init_parser,
        "track": track_parser,
        "snap": snap_parser,
        "rename": rename_parser,
        "remove": remove_parser,
        "history": history_parser,
        "show": show_parser,
        "jump": jump_parser,
        "status": status_parser,
        "amend": amend_parser,
    }

    args = parser.parse_args()

    if args.help:
        print_usage(parser, subparsers)
        sys.exit(0)

    if not args.command:
        print_usage(parser, subparsers)
        sys.exit(1)

    return args


def print_usage(parser: argparse.ArgumentParser, subparsers: dict[str, argparse.ArgumentParser]) -> None:
    print("=== Main Help ===")
    parser.print_help()

    for name, subparser in subparsers.items():
        print(f"\n=== Subcommand: {name} ===")
        subparser.print_help()


def handle_command() -> None:
    """Handle memov commands"""
    args = parse_args()

    command = args.command
    args.loc = os.path.abspath(args.loc)

    # Skip mem check for init command
    skip_mem_check = command == "init"
    manager = MemovManager(project_path=args.loc, only_basic_check=skip_mem_check)

    # Configure logging
    if not skip_mem_check:
        log_path = os.path.join(args.loc, ".mem", "mem.log")
        new_file_handler = logging.FileHandler(log_path, mode="a")
        new_file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(name)s:%(lineno)s - %(message)s")
        )
        root_logger = logging.getLogger()
        root_logger.addHandler(new_file_handler)

    if command == "init":
        manager.init()
    elif command == "track":
        manager.track(args.file_paths, args.prompt, args.response, args.by_user)
    elif command == "snap":
        manager.snapshot(args.prompt, args.response, args.by_user)
    elif command == "rename":
        manager.rename(args.old_path, args.new_path, args.prompt, args.response, args.by_user)
    elif command == "remove":
        manager.remove(args.file_path, args.prompt, args.response, args.by_user)
    elif command == "history":
        manager.history()
    elif command == "show":
        manager.show(args.prompt_id)
    elif command == "jump":
        manager.jump(args.prompt_id)
    elif command == "status":
        manager.status()
    elif command == "amend":
        manager.amend_commit_message(args.commit_hash, args.prompt, args.response, args.by_user)
    else:
        raise ValueError(f"Unknown command: {command}")


def main() -> None:
    """Main entry point for the memov command"""
    handle_command()


if __name__ == "__main__":
    main()
