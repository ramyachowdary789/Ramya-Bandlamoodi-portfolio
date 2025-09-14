import os
import json
from github import Github

# === Step 1: Ask for GitHub info ===
github_token = input("Enter your GitHub Personal Access Token: ").strip()
repo_name = input("Enter repository name (e.g., my-portfolio): ").strip()
g = Github(github_token)
user = g.get_user()

# === Step 2: Collect profile details ===
profile_data = {}
profile_data["name"] = input("Enter your full name: ").strip()
profile_data["tagline"] = input("Enter a tagline (e.g., AI Enthusiast | Developer): ").strip()
profile_data["about"] = input("Write a short About Me: ").strip()

# === Step 3: Skills ===
skills = []
print("\nEnter your skills (leave blank to finish):")
while True:
    skill = input("Skill: ").strip()
    if not skill:
        break
    skills.append(skill)
profile_data["skills"] = skills

# === Step 4: Projects ===
projects = []
print("\nEnter your projects (leave blank name to finish):")
while True:
    pname = input("Project Name: ").strip()
    if not pname:
        break
    pdesc = input("Project Description: ").strip()
    plink = input("Project Link (GitHub/live demo): ").strip()
    projects.append({"name": pname, "desc": pdesc, "link": plink})
profile_data["projects"] = projects

# === Step 5: Education ===
education = []
print("\nEnter your education history (leave blank degree to finish):")
while True:
    degree = input("Degree (e.g., SSC, Intermediate, B.Tech, Masters): ").strip()
    if not degree:
        break
    school = input(f"School/College for {degree}: ").strip()
    year = input(f"Year of completion for {degree}: ").strip()
    details = input(f"Details (marks/grade/etc.) for {degree}: ").strip()
    education.append({
        "degree": degree,
        "school": school,
        "year": year,
        "details": details
    })
profile_data["education"] = education

# === Step 6: Colors ===
print("\nChoose custom colors (press Enter for defaults):")
bg_color = input("Background color (default #0f1724): ").strip() or "#0f1724"
accent_color = input("Accent color (default #06b6d4): ").strip() or "#06b6d4"
text_color = input("Text color (default #e6eef6): ").strip() or "#e6eef6"
profile_data["colors"] = {
    "bg": bg_color,
    "accent": accent_color,
    "fg": text_color
}

# === Step 7: Save profile.json locally ===
with open("profile.json", "w") as f:
    json.dump(profile_data, f, indent=2)

print("\n✅ Profile data saved to profile.json")

# === Step 8: Create or use repo ===
try:
    repo = user.create_repo(repo_name, private=False)
    print(f"✅ Repository {repo_name} created.")
except Exception:
    repo = user.get_repo(repo_name)
    print(f"ℹ️ Repository {repo_name} already exists. Using existing one.")

# === Step 9: Prepare index.html ===
with open("template.html", "r") as f:
    html_template = f.read()

# Replace placeholders with PROFILE JSON
html_final = html_template.replace(
    "const PROFILE = {};",
    f"const PROFILE = {json.dumps(profile_data, indent=2)};"
)

with open("index.html", "w") as f:
    f.write(html_final)

print("✅ index.html generated with your data")

# === Step 10: Push to GitHub ===
os.system("git init")
os.system(f"git remote add origin https://github.com/{user.login}/{repo_name}.git")
os.system("git branch -M main")
os.system("git add .")
os.system('git commit -m "Initial portfolio commit"')
os.system("git push -u origin main --force")

print("\n🚀 Your portfolio has been deployed!")
print(f"🔗 Visit: https://{user.login}.github.io/{repo_name}/")
