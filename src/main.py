import argparse
import os
import sys
from dotenv import load_dotenv
from streamlit.web import cli as stcli
from utils.process import process

# Load environment variables from a .env file
load_dotenv()


def process_docs(args):
    """
    Process a Confluence space and store the results in Bedrock
    """
    process(
      args.confluence_space_key,
      os.environ.get("CONFLUENCE_URL"),
      os.environ.get("CONFLUENCE_USERNAME"),
      os.environ.get("CONFLUENCE_API_KEY")
    )


def chat(args):
    """
    Start the Streamlit chat application using the specified Activeloop dataset.
    """
    activeloop_username = os.environ.get("ACTIVELOOP_USERNAME")

    args.activeloop_dataset_path = (
        f"hub://{activeloop_username}/{args.activeloop_dataset_name}"
    )

    sys.argv = [
        "streamlit",
        "run",
        "src/utils/chat.py",
        "--",
        f"--activeloop_dataset_path={args.activeloop_dataset_path}",
    ]

    sys.exit(stcli.main())


def main():
    """Define and parse CLI arguments, then execute the appropriate subcommand."""
    parser = argparse.ArgumentParser(description="Chat with Confluence Docs")
    subparsers = parser.add_subparsers(dest="command")

    # Process subcommand
    process_parser = subparsers.add_parser("process", help="Process a Confluence space")
    process_parser.add_argument(
        "--confluence_space_key", required=True, help="Confluence space key"
    )

    # Chat subcommand
    chat_parser = subparsers.add_parser("chat", help="Start the chat application")
    chat_parser.add_argument(
        "--activeloop-dataset-name",
        required=True,
        help="The name of one of your existing Activeloop datasets.",
    )

    args = parser.parse_args()

    if args.command == "process":
        process_docs(args)
    elif args.command == "chat":
        chat(args)


if __name__ == "__main__":
    main()
