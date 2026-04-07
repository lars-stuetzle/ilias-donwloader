import os
import re
import json
import urllib.parse
from bs4 import BeautifulSoup
from .auth import get_ilias_session

BASE_URL = "https://ilias.uni-konstanz.de/"

def sync_ilias_folder(session, url, local_dir, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()
        
    if url in visited_urls:
        return
    visited_urls.add(url)
    
    print(f"\n📂 Scanning: {local_dir}")
    os.makedirs(local_dir, exist_ok=True)
    
    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    for link in soup.find_all('a'):
        text = link.get_text(strip=True)
        href = link.get('href')
        
        if not text or not href or len(text) < 2:
            continue
            
        full_url = urllib.parse.urljoin(BASE_URL, href)
        
        if "cmd=sendfile" in full_url:
            file_response = session.get(full_url)
            content_disposition = file_response.headers.get('content-disposition', '')
            
            real_filename = None
            if 'filename=' in content_disposition:
                found_names = re.findall('filename="?([^"]+)"?', content_disposition)
                if found_names:
                    real_filename = found_names[0]
                    
            if not real_filename:
                safe_name = re.sub(r'[\\/*?:"<>|]', "", text)
                real_filename = f"{safe_name}.pdf" 
                
            file_path = os.path.join(local_dir, real_filename)
            
            if not os.path.exists(file_path):
                print(f"  ⬇️ Downloading new file: {real_filename}")
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)
            else:
                print(f"  ⏭️ Already exists: {real_filename}")
                
        elif "/fold/" in full_url and full_url not in visited_urls:
            safe_folder_name = re.sub(r'[\\/*?:"<>|]', "", text)
            new_local_dir = os.path.join(local_dir, safe_folder_name)
            sync_ilias_folder(session, full_url, new_local_dir, visited_urls)

def main():
    print("Initializing ILIAS Downloader...")
    
    # --- CONFIGURATION ---
    # PASTE YOUR UNIVERSITY FOLDER PATH HERE
    # Example: "C:/Users/stutz/Documents/University/Summer_Semester_2026"
    BASE_OUTPUT_PATH = r"C:\Users\stutz\OneDrive\Desktop\SEDS\2. Semester"
    
    # Path to your courses.json (assumed to be in the same folder as the script/terminal)
    current_dir = os.getcwd()
    json_path = os.path.join(current_dir, "courses.json")

    if not os.path.exists(json_path):
        print(f"❌ Error: 'courses.json' not found in: {current_dir}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        courses_to_sync = json.load(f)
    
    my_session = get_ilias_session()
    
    if my_session:
        print(f"\n🚀 Files will be saved to: {BASE_OUTPUT_PATH}")
        
        for folder_name, course_url in courses_to_sync.items():
            # Create a safe path for the course folder inside your Uni folder
            safe_course_name = re.sub(r'[\\/*?:"<>|]', "", folder_name)
            course_local_dir = os.path.join(BASE_OUTPUT_PATH, safe_course_name)
            
            print(f"\n" + "="*50)
            print(f"🔄 Processing course: {safe_course_name}")
            print("="*50)
            
            sync_ilias_folder(my_session, course_url, course_local_dir)
            
        print("\n🎉 All courses are up to date!")
    else:
        print("❌ Could not establish a session. Aborting.")

if __name__ == "__main__":
    main()