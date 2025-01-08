import argparse
import os
from dotenv import load_dotenv
import praw
import pandas as pd
import time


# Загрузка переменных из .env файла
load_dotenv()


def get_unique_filename(base_filename):
    """
    Generate a unique filename by appending a number if the file already exists.
    """
    if not os.path.exists(base_filename):
        return base_filename

    # Split the base filename into name and extension
    name, ext = os.path.splitext(base_filename)
    counter = 1

    # Keep incrementing the counter until a unique filename is found
    while os.path.exists(f"{name}_{counter}{ext}"):
        counter += 1

    return f"{name}_{counter}{ext}"


def get_reddit_instance():
    reddit = praw.Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID'),
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
        user_agent=os.environ.get('REDDIT_USER_AGENT'),
        username=os.environ.get('REDDIT_USERNAME'),
        password=os.environ.get('REDDIT_PASSWORD')
    )
    return reddit


# Function to check post details
def check_post(reddit, url):
    try:
        submission = reddit.submission(url=url)
        if submission.locked:
            return {
                "url": url,
                "comment_count": "locked"
            }
        elif submission.archived:
            return {
                "url": url,
                "comment_count": "archived"
            }

        comment_count = submission.num_comments
        return {
            "url": url,
            "comment_count": comment_count
        }
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None


def process_urls_with_reddit(file_path, output_file_path="output.xlsx", batch_size=100):
    """
    Processes a URLs Excel file, retrieves Reddit post details for URLs, and saves the results to an output Excel file.

    Args:
        file_path (str): Path to the input URLs Excel file containing columns "URL" and "Traffic with commercial intents in top 20".
        output_file_path (str): Path to the output Excel file where processed results will be saved. Default is "output.xlsx".
        batch_size (int): Number of URLs to process before pausing to respect Reddit API rate limits. Default is 100.

    Steps:
        1. Reads the input Excel file and extracts URLs and their associated traffic data.
        2. Initializes a Reddit instance for API interaction.
        3. Iterates through the list of URLs:
            - Fetches Reddit post details (e.g., comment count) using the `check_post` function.
            - Skips locked or archived posts.
        4. Pauses processing after every `batch_size` URLs to avoid hitting Reddit API rate limits.
        5. Saves the processed data to an Excel file with a unique filename if the default output file already exists.

    The output file contains:
        - "url": The processed URL.
        - "traffic": Traffic value from the input file for the corresponding URL.
        - "comment_count": The number of comments retrieved from Reddit.

    Raises:
        FileNotFoundError: If the input file is not found.
        ValueError: If required columns are missing from the input file.
        Exception: If any other errors occur during processing.

    Returns:
        None
    """
    try:
        # Generate a unique output file name if necessary
        output_file_path = get_unique_filename(output_file_path)

        # Read SEMrush data
        semrush_data = pd.read_excel(file_path)

        # Validate required columns
        required_columns = {"URL", "Traffic with commercial intents in top 20"}
        missing_columns = required_columns - set(semrush_data.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        urls = semrush_data["URL"].tolist()
        traffic_data = semrush_data.set_index("URL")["Traffic with commercial intents in top 20"].to_dict()

        output_data = []

        # Reuse the same instance
        reddit_instance = get_reddit_instance()

        for i, url in enumerate(urls, 1):
            # Print the current progress
            print(f"Processing {i}/{len(urls)}: {url}")

            result = check_post(reddit_instance, url)
            if result is not None:
                output_data.append(
                    {
                        "url": result["url"],
                        "traffic": traffic_data[result["url"]],
                        "comment_count": result["comment_count"]
                    }
                )

            # Sleep to respect Reddit API rate limits
            if i % batch_size == 0:
                print(
                    f"Processed {i}/{len(urls)} URLs. Sleeping for 1 minute to avoid rate limits.")
                time.sleep(60)

        # Save results to excel
        output_df = pd.DataFrame(output_data)
        output_df.to_excel(output_file_path, index=False, engine='openpyxl')

        print(f"Process completed. Results saved to --> {output_file_path}.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Process an Excel file with URLs and traffic data."
    )

    # Define a positional argument for the input file
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input Excel file containing URL and Traffic data.",
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the input file path
    input_file = args.input_file

    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        exit(1)

    # Call the processing function with the input file
    process_urls_with_reddit(input_file)
