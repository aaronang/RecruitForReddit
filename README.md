# RecruitForReddit

## Getting started

> Note: This script won't work with a newly created account as it can't send private messages.

### Getting API access

1. Go to [apps settings](https://www.reddit.com/prefs/apps).
1. Click on "create another app..." all the way at the bottom of the page.
1. Provide a name.
1. Select "script".
1. Provide a short description.
1. You can skip the about url.
1. Use `http://localhost:8080` for the redirect uri.
1. Click "create app".
   > Note down the OAUTH Client ID right below "personal use script" and if you click on "edit" on the app that you just created, you can find the `secret` that will we have to use later.
1. Go to [Reddit API Terms of Use](https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform) and fill out the form.

### Running the code

1. Rename the `.env.example` file to `.env`.
1. Fill in the values in `.env`.
1. Update `SUBREDDIT_NAME`, `SUBJECT_LINES`, `MESSAGE_TEMPLATE`, and the line below the `TODO` in `main.py`.
1. Run the code:
   ```
   py main.py
   ```