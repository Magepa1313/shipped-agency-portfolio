git add .
git commit -m "Initial commit for Shipped agency website"
git branch -M main
gh repo create shipped-agency-portfolio --public --source=. --remote=origin --push
