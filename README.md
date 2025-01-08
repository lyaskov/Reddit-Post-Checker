# Reddit Post Checker

## 📖 Description
A script to process URLs from an Excel file, retrieve Reddit post details, and save the results to a new Excel file. Handles rate limits and ensures unique output filenames.

---

## ✨ Features
- Reads Excel files with `URL` and `Traffic with commercial intents in top 20`.
- Retrieves Reddit post details like comment counts.
- Identifies blocked or archived messages.
- Automatically generates unique output filenames.

---

## 🛠️ Requirements
- Python 3.7+
- Install dependencies:
  ```bash
  pip install -r requirements.txt



## 🚀 Usage

### Clone the repo:
```bash
git clone https://github.com/your-username/reddit-post-checker.git
```

### Configure .env with Reddit API credentials:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
```

### Run the script:
```bash
python script_name.py <input_file>
```

## 📋 Example
- **Input**: Excel file with columns:
  - `URL`: Reddit post URLs.
  - `Traffic with commercial intents in top 20`: Traffic data associated with the URLs.
- **Output**: Excel file with columns:
  - `url`: The Reddit post URL.
  - `traffic`: Traffic value from the input file.
  - `comment_count`: The number of comments for the Reddit post or its status (`archived`/`locked`).

## 📝 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

## 👤 Author
Created by **lyaskov**.
