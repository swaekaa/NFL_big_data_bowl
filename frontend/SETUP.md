# Run this script to set up and launch the NFL Big Data Bowl 2027 frontend
# Step 1: Export data
cd c:\Users\Ekaansh\OneDrive\Desktop\AB\projects\nfl\nfl-bdb-2027
.\venv\Scripts\python.exe scratch\export_frontend_data.py

# Step 2: Install npm packages
cd frontend
npm install

# Step 3: Start dev server
npm run dev
