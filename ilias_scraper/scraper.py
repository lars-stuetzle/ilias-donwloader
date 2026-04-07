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
                print(f"  ⬇️ Downloading: {real_filename}")
                with open(file_path, 'wb') as f:
                    f.write(file_response.content)
            else:
                print(f"  ⏭️ Skipping: {real_filename}")
                
        elif "/fold/" in full_url and full_url not in visited_urls:
            safe_folder_name = re.sub(r'[\\/*?:"<>|]', "", text)
            new_local_dir = os.path.join(local_dir, safe_folder_name)
            sync_ilias_folder(session, full_url, new_local_dir, visited_urls)

def main():
    print("Initializing ILIAS Downloader...")
    
    # Load configuration
    json_path = os.path.join(os.getcwd(), "courses.json")
    if not os.path.exists(json_path):
        print(f"❌ Error: 'courses.json' not found in {os.getcwd()}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # PRIVACY FIX: Get the output path from the ignored JSON file
    # If not found, default to a 'downloads' folder in the current directory
    base_output = config.get("output_path", "downloads")
    
    my_session = get_ilias_session()
    
    if my_session:
        print(f"\n🚀 Target Directory: {base_output}")
        
        for key, value in config.items():
            if key == "output_path":
                continue # Skip the path setting
                
            safe_name = re.sub(r'[\\/*?:"<>|]', "", key)
            course_dir = os.path.join(base_output, safe_name)
            
            print(f"\n" + "="*50)
            print(f"🔄 Syncing: {safe_name}")
            print("="*50)
            sync_ilias_folder(my_session, value, course_dir)
            
        print("\n🎉 Sync Complete!")
    else:
        print("❌ Login failed.")

if __name__ == "__main__":
    main()