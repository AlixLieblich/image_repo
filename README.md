## 🔭 National Treaures Image Repository 🌠

## For Shopify Fall 2021 Backend Developer Internship

###  👽 Overview

National Treasures is a image repository developed for the Shopify Fall 2021 Backend Developer Internship.
This project was developed by me, Alix Lieblich, while still a fellow of the Hackbright Academy Fullstack Software Engineering Bootcamp. My features chosen for the image repository are adding images to the repository via user profiles, deleting images via user profiles, and adding images from the gallery to a user's own profile. 

### 🖥️ Technologies required 

- Python, Javascript, HTML, CSS, Bootstrap, PostgreSQL, Flask, and Flask-Login. 

### 🌌 Data

- Seeded Database with fake users and images seeded using seed_database.py.

### 🌜 User Accounts

- Users are able to create accounts via the Sign Up page. By having users fill out a form with basic contact info, an account is created using Flask retrieval method ```request.form.get```. With user info collected, an account is finalized by using a function from crud.py which utilizes the PostgreSQL model in order to the user to the database.
```
def create_user(username, password, user_fname, user_lname, email, profile_picture="/static/img/profile_pictures/default.png"):
    """Create and return a new user."""

    user = User(username=username, password=password, user_fname=user_fname, user_lname=user_lname, profile_picture=profile_picture, email=email)

    db.session.add(user)
    db.session.commit()

    return user
```
![Image of User Sign Up](filteredFlats.png)


### 📷 Uploading an Image

- When a user is signed into their account, they can access their profile on which they are able to upload an image.
![Image of User Profile](filteredFlats.png)

### Deleting an Image

-Where users can view their images, they are also able to delete them. The images are deleted using the Flask delete function.
```
@app.route('/profile_edit', methods = ["POST"])
def edit_user_profile():
    """Edit user profile with user form responses."""

# if user is not logged in, redirect them to the login page
    if not current_user.is_authenticated:
        return redirect('/create-account')
# collect the users id using Flask-Login function 'current_user'
    user_id = current_user.user_id
    user_object = User.query.get(user_id)
   
    form_id = request.form.get("form_id")

    #delete image
    if form_id == "delete_image":
        image_id = request.form.get("image_id")
        Image.query.filter(Image.image_id==image_id).delete()
        db.session.commit()

        return redirect("user_profile")
```
![Image of Where to Delete Image](filteredFlats.png)

### Adding an image from the Gallery of all images on the site

- When a user is viewing the gallery of all images from all users, they have the option to add a photo to their profile. When a user clicks the radio button and hits submit, the image name as well as the three tag variables are collected from their hidden places on the form and are used to create a new image object for the user's profile using the same route as that to delete an image from the user's profile.
```
@app.route('/profile_edit', methods = ["POST"])
def edit_user_profile():
    """Edit user profile with user form responses."""

# if user is not logged in, redirect them to the login page
    if not current_user.is_authenticated:
        return redirect('/create-account')
# collect the users id using Flask-Login function 'current_user'
    user_id = current_user.user_id
    user_object = User.query.get(user_id)
   
    form_id = request.form.get("form_id")
    
    #add image from gallery
    if form_id == "add_from_gallery":
        image_name = request.form.get("image_name")
        tag1 = request.form.get("tag1")
        tag2 = request.form.get("tag2")
        tag3 = request.form.get("tag3")

        crud.create_image(user_id, image_name, tag1, tag2, tag3)
```
![Image of Where to Add Image from Gallery](filteredFlats.png)
