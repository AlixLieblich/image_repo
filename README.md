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

*crud.py*
```
def create_user(username, password, user_fname, user_lname, email, profile_picture="/static/img/profile_pictures/default.png"):
    """Create and return a new user."""

    user = User(username=username, password=password, user_fname=user_fname, user_lname=user_lname, profile_picture=profile_picture, email=email)

    db.session.add(user)
    db.session.commit()

    return user
```

![Image of User Sign Up](/static/img/readme/create-account.png)


### 📷 Uploading an Image

- When a user is signed into their account, they can access their profile on which they are able to upload an image. The image is uploaded using is form which requires the three tags be filled out, in addition to a jpg image be uploaded. A function from crud.py is then used to create the image object for the user account.

*crud.py*
```
def create_image(user_id, image_name, tag1, tag2, tag3):
    """Create an Image object."""

    image = Image(user_id=user_id, image_name=image_name, tag1=tag1, tag2=tag2, tag3=tag3)

    db.session.add(image)
    db.session.commit()

    return image

```

![Image of User Profile](/static/img/readme/user__profile.png)

### Deleting an Image

-Where users can view their images, they are also able to delete them. The images are deleted using the Flask delete function. Extra care was taken for security so that only a user can delete their own images by ensuring that the user who is logged in matches the id of the user deleting the image.

*server.py*
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

![Image of Where to Delete Image](/static/img/readme/user_profile.png)

### Adding an image from the Gallery of all images on the site

- When a user is viewing the gallery of all images from all users, they have the option to add a photo to their profile. When a user clicks the radio button and hits submit, the image name as well as the three tag variables are collected from their hidden places on the form and are used to create a new image object for the user's profile using the same route as that to delete an image from the user's profile.

*server.py*
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

![Image of Where to Add Image from Gallery](/static/img/readme/all_images.png)

### Searching the whole site by tags

- A user may use the search bar from the navbar to search for images by the tags they are uploaded with. This is accomplished by creating an input box with a submit button and Bootstrap classes, then getting the users query using Flask retrieval method ```request.form.get```. With the query gathered, the database is searched for the query and the results are returned on a separate page.

*server.py*
```
@app.route('/search_bar', methods = ["POST"])
def search_bar():
    """Use navbar search bar."""

    search_query = request.form.get('search_query')

    search_query = db.session.query(Image).filter(Image.tag1==search_query).all()
    if search_query == None:
        search_query = db.session.query(Image).filter(Image.tag2==(search_query)).all()
        if search_query == None:
            search_query = db.session.query(Image).filter(Image.tag3==(search_query)).all()
    
    return render_template('show-form.html',
                            search_query=search_query)
```

![Image of Search Results](/static/img/readme/search_results.png)

### Flask Testing

- Flask testing methods are used as well in tests.py .

*tests.py*
```
class FlaskTestCase(TestCase):
    def setUp(self):
        """Routine before test starts."""

        #Get Flask test client
        self.client = app.test_client
        #Show errors from Flask than happen
        app.config['TESTING'] = True
        #Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        #Create tables and add sample data to them
        db.create_all()
        example_data()

    def tearDown(self):
        """To be done at the end of every test."""

        db.session.close()
        db.drop_all()

    def test_user(self):
        """Test for user in test data."""

        user = User.query.filter(User.user_fname == "Smokey").first()
        self.assertEqual(user.user_fname, "Smokey")

    def test_image(self):
        """Test for image in test data."""

        image = Image.query.filter(Image.tag1 == "Denali").first()
        self.assertEqual(image.tag1, "Denali")
```