An Online Market for IT products.

- clone the repo to your PC.
- pip install -r requirements.txt.

Current state:
    - can register users.
    - uses a login system.
    - users can edit/delete their own profile.
    - can add admins.
    - admins can add/edit/delete products.
    - admins can edit/delete other users.
    - products presentation page.
    - working contact page.

HOW TO USE:

    AS A NORMAL USER:
        - first you have to go to the registration page to create an account.
        - click on "Register" and complete the form.
        - after you have created an account you get a dashboard where you can edit or delete your profile.
        EDITING normal user profile:
            - go to your dashboard.
            - click on "Edit Profile" button.
            - on the form that drops down you can edit some of your profile info.
        DELETEING normal user profile:
            - go to your dashboard.
            - click on "Edit Profile" button.
            - click on "Delete Profile" button(the red one on the right).
        - on the Products page you can check the existing products.

    AS AN ADMIN:
        - admins can do more things than normal users from obvious reasons. :)
        - first you need to create an admin account.
        - first registered account is set by default to be admin.
        - once you have created your admin account you can go to your admin dashboard.
        - from your dashboard you can edit your personal admin account as a normal user can.
        - from the "Edit/Add Products" page you can add, edit or even delete a product from the database.
        - from "Edit Users" page you can edit or delete existing users.
        EDITING A PRODUCT:
            - go to "Edit/Add Products" page.
            - click on the name of the product you want to edit.
            - on the appearing form complete the entry that you want to change and click on "Update Product" button.
        DELETING A PRODUCT:
            - go to "Edit/Add Products" page.
            - click on the name of the product you want to delete.
            - click on the "Delete Product" button on the right.
        ADDING A NEW PRODUCT:
            - first add a picture of your product in static/images.
            - the picture has to be .png
            - go to "Edit/Add Products" page.
            - on the right side, click on the "Add Product" button.
            - complete the form that appears and press "Add Product" at the end.
            - in the "Image source" entry box you need to specify the address of a product
            picture(e.g. main_directory/static/images/Laptop Gaming ASUS TUF A15 FA506IHR-HN039.png)
        EDITING A USER:
            - to edit a user go to "Edit Users" page and click on the full name of the user that you want to edit.
            - in the appearing form change the details that you want, then click on the "Update Profile" button.
        DELETEING A USER:
            - as admin you also can delete other users.
            - go to "Edit Users" page and click on the full name of the user that you want to delete.
            - on the appearing form just hi the "Delete Profile" button to delete that user's profile.




