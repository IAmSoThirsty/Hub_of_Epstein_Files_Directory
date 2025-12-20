# Deployment Guide - Getting Your Site Live

## 🚀 Quick Deployment (5-10 minutes)

This guide will walk you through publishing the Epstein Files Hub site on GitHub Pages for **FREE**.

---

## Step 1: Enable GitHub Pages (2 minutes)

1. Go to your repository: `https://github.com/IAmSoThirsty/Hub_of_Epstein_Files_Directory`
2. Click **Settings** (top right)
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select:
   - **Branch**: `copilot/create-self-organizing-workflow` (or `main` after merge)
   - **Folder**: `/web` (this is important!)
5. Click **Save**

✅ GitHub will show a message: "Your site is ready to be published at..."

**Wait 2-3 minutes** for the build to complete.

---

## Step 2: Verify Deployment (1 minute)

1. Your site will be live at:
   ```
   https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/
   ```

2. Test these pages:
   - Home: `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/index.html`
   - Search: `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/search.html`
   - Characters: `https://iamsothirsty.github.io/Hub_of_Epstein_Files_Directory/characters.html`

---

## Step 3: Optional - Custom Domain (5 minutes)

If you want a custom domain like `epsteinfiles.org`:

1. Buy domain from provider (Namecheap, Google Domains, etc.)
2. In GitHub Settings → Pages → Custom domain, enter: `epsteinfiles.org`
3. Add these DNS records at your domain provider:
   ```
   Type: CNAME
   Name: www
   Value: iamsothirsty.github.io
   
   Type: A
   Name: @
   Values:
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```
4. Wait 24-48 hours for DNS propagation

---

## Step 4: Fetch Public Files (Optional - 2 hours)

If you want to populate the site with FBI Vault files:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# Install system dependencies
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr poppler-utils

# macOS:
brew install tesseract poppler

# 2. Fetch FBI Vault files (22 PDFs)
python scripts/fetch-public-files.py
# Select "FBI Vault" when prompted

# 3. Process PDFs (text extraction + OCR)
python scripts/process-pdfs.py

# 4. Generate search index
python scripts/generate-search-index.py

# 5. Commit and push
git add data/ web/js/search-index.js
git commit -m "Add FBI Vault documents and search index"
git push
```

Wait 2-3 minutes for GitHub Pages to rebuild.

---

## Step 5: Enable Automated Updates (Optional - 5 minutes)

The repository includes workflows that will automatically fetch and process files monthly.

**No action needed!** The workflows are already configured in `.github/workflows/`:
- `fetch-public-files.yml` - Monthly FBI/DOJ file fetching
- `update-search-index.yml` - Weekly search index updates

You can also trigger them manually:
1. Go to **Actions** tab
2. Select workflow (e.g., "Fetch and Process Public Files")
3. Click **Run workflow**

---

## Troubleshooting

### Site not loading after 5 minutes?
- Check **Actions** tab for build errors
- Verify **Settings → Pages** shows "Your site is published"
- Try clearing browser cache (Ctrl+Shift+R)

### Search not working?
- Make sure you've generated the search index: `python scripts/generate-search-index.py`
- Check that `web/js/search-index.js` exists
- Open browser console (F12) to check for JavaScript errors

### 404 errors on navigation?
- Ensure GitHub Pages source is set to `/web` folder, not root
- Check that all file paths are relative (no leading `/`)

### Files too large for GitHub?
- Use Git LFS for files > 50MB: `git lfs track "*.pdf"`
- Or host large files externally (Archive.org, Cloudflare R2)

---

## Performance Optimization

### Enable Cloudflare CDN (Free)
1. Sign up at cloudflare.com
2. Add your custom domain
3. Update nameservers at your domain provider
4. Enable caching and compression in Cloudflare dashboard

**Benefits:**
- Faster loading (CDN caching)
- 100GB free bandwidth
- DDoS protection
- Analytics

### Compress Images
```bash
# Install tools
npm install -g imagemin-cli

# Compress all images
imagemin web/images/* --out-dir=web/images/
```

---

## Monitoring & Analytics

### Free Options:
1. **GitHub Pages Stats**: Settings → Insights → Traffic
2. **Google Analytics**: Add tracking code to `web/index.html`
3. **Cloudflare Analytics**: Built-in if using Cloudflare

---

## Cost Summary

| Item | Cost |
|------|------|
| GitHub Pages hosting | **$0** |
| GitHub Actions (2,000 min/month) | **$0** |
| SSL certificate | **$0** (included) |
| Custom domain (optional) | $10-15/year |
| Cloudflare CDN (optional) | **$0** |
| **TOTAL** | **$0-15/year** |

**Annual savings vs. Azure full setup: $15,720+**

---

## Next Steps After Deployment

1. ✅ **Merge PR** to main branch
2. ✅ **Update GitHub Pages** source to `main` branch
3. ✅ **Share the URL** with your community
4. ✅ **Monitor traffic** and performance
5. ✅ **Add more documents** as they become available
6. ✅ **Set up custom domain** (optional)

---

## Support

If you encounter issues:
1. Check the [FREE_TIER_SETUP.md](FREE_TIER_SETUP.md) guide
2. Review [PUBLIC_FILES_INTEGRATION.md](PUBLIC_FILES_INTEGRATION.md)
3. Open an issue on GitHub
4. Check GitHub Pages documentation

---

## Success Checklist

After deployment, verify these work:

- [ ] Home page loads
- [ ] Search page loads
- [ ] Search functionality works (try searching "Little St. James")
- [ ] Character guide loads
- [ ] Locations page loads
- [ ] Infographics page loads
- [ ] Navigation works between pages
- [ ] Mobile responsive design works
- [ ] HTTPS certificate active (padlock in browser)

---

**Congratulations! Your FREE Epstein Files Hub is now live! 🎉**

**Monthly cost: $0 | Setup time: 5-10 minutes | Annual savings: $15,720+**
