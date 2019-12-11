**PyCharm is my favorite Python IDE-:).**

# 1. Start PyCharm

Make sure you have activated your virtual environment. If not, run the command within `Projfect_Folder` directory:

```
. venv/bin/activate
```

Then start PyCharm:

```
pycharm .
```

# 2. Mark `./code` as **Source Folders**

Since we will put all your python scripts in the `./code`, we need to tell PyCharm that this is a **Source Folder**. Otherwise PyCharm will have some **Unresolved Reference** issues.

Go to PyCharm **Preferences -> Project Structure**, select the `code` folder, and then cleck **Sources** on the top of the window. 

# 3. Local Data Science Coding

The principle of **Data Science in AWS** is that we use a small subset of data to develop our data science workflow locally, and then move the work to AWS for scaling up.
