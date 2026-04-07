# ILIAS Course Downloader 🎓

An automated tool to synchronize course materials from ILIAS (University of Konstanz) to your local machine. This tool handles the login, scans all subfolders, and downloads new files while skipping existing ones.

## 🚀 Features

* **Automated Sync**: Maintains the exact folder structure from ILIAS.
* **Smart Updates**: Only downloads what you don't already have.
* **Customizable**: Keep your code separate from your study materials.

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/YOUR_USERNAME/ilias-downloader.git
   cd ilias-downloader
   ```

2. **Install as a package**:

   ```bash
   pip install -e .
   ```

## ⚙️ Setup

### Create `courses.json`

Create a file named `courses.json` in the project root with your course names and links:

```json
{
    "Applied Time Series": "https://ilias.uni-konstanz.de/...",
    "Machine Learning": "https://ilias.uni-konstanz.de/..."
}
```

### Set Output Path

Open `ilias_scraper/scraper.py` and update the `BASE_OUTPUT_PATH` variable to your desired university folder (e.g., `C:/Users/Name/Documents/University`).

## 📁 Usage

Once configured, simply run:

```bash
ilias-sync
```

A browser window will open for the university login. After you log in, the script will handle the rest!

## 🔒 Notes

* Your `courses.json` and downloaded files are ignored by Git for privacy.
