# ILIAS Course Downloader 🎓

An automated tool to synchronize course materials from ILIAS (University of Konstanz) to your local machine. This tool handles the login, scans all subfolders, and downloads new files while skipping existing ones.

## 🚀 Features
- **Automated Sync**: Maintains the exact folder structure from ILIAS.
- **Smart Updates**: Only downloads what you don't already have.
- **Privacy First**: Keep your folder paths and course links in a private config file.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lars-stuetzle/ilias-downloader.git
   cd ilias-downloader
   ```

2. **Install as a package**:
   ```bash
   pip install -e .
   ```

## ⚙️ Setup

### Create `courses.json`

Create a file named `courses.json` in the project root folder. This file is ignored by Git (via `.gitignore`), so your data stays private.

```json
{
    "output_path": "C:/Users/YourName/Documents/University/...",
    "Course Name 1": "https://ilias.uni-konstanz.de/...",
    "Course Name 2": "https://ilias.uni-konstanz.de/..."
}
```

## 📁 Usage

Simply run the following command in your terminal:

```bash
ilias-sync
```

A browser window will open for the university login. After you log in, the script will handle the rest!
