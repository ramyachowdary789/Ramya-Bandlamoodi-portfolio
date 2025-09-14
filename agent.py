import os
import json
import shutil
from getpass import getpass
from github import Github, GithubException

# --- 1. Collect user info ---
print("=== GitHub Info ===")
github_username = input("GitHub Username: ")
github_token = getpass("GitHub Personal Access Token: ")

print("\n=== Portfolio Info ===")
name = input("Full Name: ")
tagline = input("Tagline (e.g., Full Stack Developer): ")
about = input("About Yourself: ")

skills = input("Skills (comma separated): ").split(",")
projects = []
while True:
    add_proj = input("Add a project? (y/n): ").lower()
    if add_proj != "y":
        break
    pname = input("Project Name: ")
    pdesc = input("Project Description: ")
    plink = input("Project Link: ")
    projects.append({"name": pname, "desc": pdesc, "link": plink})

education = []
while True:
    add_edu = input("Add education? (y/n): ").lower()
    if add_edu != "y":
        break
    degree = input("Degree (e.g., B.Tech, SSC): ")
    school = input("School/College: ")
    year = input("Year/Duration: ")
    details = input("Additional Details (optional): ")
    education.append({"degree": degree, "school": school, "year": year, "details": details})

print("\n=== Theme Colors ===")
bg = input("Background color (hex, default #0f1724): ") or "#0f1724"
accent = input("Accent color (hex, default #06b6d4): ") or "#06b6d4"
fg = input("Text color (hex, default #e6eef6): ") or "#e6eef6"

profile = {
    "name": name,
    "tagline": tagline,
    "about": about,
    "skills": [s.strip() for s in skills],
    "projects": projects,
    "education": education,
    "colors": {"bg": bg, "accent": accent, "fg": fg}
}

# --- 2. Save profile.json ---
with open("profile.json", "w", encoding="utf-8") as f:
    json.dump(profile, f, indent=2)
print("✅ profile.json created.")

# --- 3. Generate index.html from template ---
if not os.path.exists("template.html"):
    print("❌ template.html not found! Place it in the same folder as agent.py")
    exit(1)

with open("template.html", "r", encoding="utf-8") as f:
    template_html = f.read()

# Inject profile as JS object
profile_js = f"<script>const PROFILE = {json.dumps(profile)};</script>"
index_html = template_html.replace("// This will be replaced dynamically by agent.py", profile_js)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print("✅ index.html generated from template.")

# --- 4. Connect to GitHub ---
try:
    g = Github(github_token)
    user = g.get_user()
except GithubException as e:
    print("❌ GitHub authentication failed:", e)
    exit(1)

# --- 5. Create or get repository ---
repo_name = f"{name.replace(' ', '-')}-portfolio"
try:
    repo = user.create_repo(repo_name)
    print(f"Repository '{repo_name}' created.")
except GithubException as e:
    if e.status == 422:  # Already exists
        repo = g.get_user().get_repo(repo_name)
        print(f"Repository '{repo_name}' already exists. Using existing repo.")
    else:
        print("❌ Repo creation failed:", e)
        exit(1)

# --- 6. Save files in repo root ---
# Remove any leftover nested .git in deployments folder if exists
deployments_folder = "deployments"
if os.path.exists(deployments_folder):
    shutil.rmtree(deployments_folder)

# Files are already created in root: index.html, profile.json
# Nothing more to copy
print("✅ index.html and profile.json are in repo root for Git tracking.")


# --- 7. Git add, commit, push ---
os.chdir(os.path.abspath("."))

if not os.path.exists(".git"):
    os.system("git init")

# Configure git user
os.system('git config --global user.name "Your Name"')
os.system('git config --global user.email "you@example.com"')

# Add all files
os.system("git add .")
os.system('git commit -m "Update portfolio deployment"')
os.system("git branch -M main")
os.system(f"git remote add origin https://github.com/{github_username}/{repo_name}.git 2>nul")
os.system("git push -u origin main --force")

print(f"\n🚀 Portfolio deployed: https://{github_username}.github.io/{repo_name}/")
