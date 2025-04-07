# Testing

Testing file for 1up GrowKits [README.md](README.md).

## Testing User Stories

### Developer Stories

- [x] Frontend and Backend of the project created.
- [x] Database is connected to the project.
- [x] App deployed on Heroku.

### User Stories

- [x] Register an account
- [x] Login & logout of account
- [x] Manage user accounts
- [x] Browse products & courses
- [x] Detailed product & course view
- [] Add featured items
- [x] Add to shopping cart
- [x] Update items in cart
- [x] Secure card payment checkout
- [x] Order summary display
- [x] Order management
- [] Successful order email
- [x] Product & course management
- [] Auto low-stock warning
- [x] Booking a course
- [] Social media profile
- [] Optimize with Google SEO


## Validation

### Validation Errors
- 

### HTML Validation Corrected

- [] HTML validation all passed:

**Home page**  
![Home Page HTML Validation](static/documentation/testing/html-home.webp)

**Login Page**  
![Login Page HTML Validation](static/documentation/testing/html-login.webp)

**Logout Page**  
![Logout Page HTML Validation](static/documentation/testing/html-logout.webp)

**Review Post Page**  
![Review Post Page HTML Validation](static/documentation/testing/html-products.webp)

**About Page**  
![About Page HTML Validation](static/documentation/testing/html-courses.webp)

### CSS Validation Corrected

- [] CSS validation all passed.

**Home page**  
![CSS Validation](static/documentation/testing/css-home.webp)

**Login Page**  
![CSS Validation](static/documentation/testing/css-login.webp)

**Signup Page**  
![CSS Validation](static/documentation/testing/css-signup.webp)

**Logout Page**  
![CSS Validation](static/documentation/testing/css-logout.webp)

**Review Post Page**  
![CSS Validation](static/documentation/testing/css-products.webp)

**About Page**  
![CSS Validation](static/documentation/testing/css-courses.webp)

### JSHint

- [] JavaScript tests all passed.

![JSHint](static/documentation/testing/jshint.webp)

### CI Python Linter

- [] Python tests all passed.

    All Python files containing the project's code have been tested. 
    All the errors were fixed, and after running the CI Python Linter, it shows there are no errors.

| **Feature** | **admin.py** | **forms.py** | **models.py** | **urls.py** | **views.py** | **test_views.py** | **test_forms.py** | **tests.py** |
| ----------- |:------------:|:------------:|:-------------:|:-----------:|:------------:|:-----------------:|:-----------------:|:------------:|
| 1up GrowKits main app | n/a | n/a | n/a | [no errors](static/documentation/testing/main-urls.webp) | n/a | n/a | n/a | n/a |
| Products | [no errors](static/documentation/testing/products-admin.webp) | [no errors](static/documentation/testing/products-forms.webp) | [no errors](static/documentation/testing/products-models.webp) | [no errors](static/documentation/testing/products-urls.webp) | [no errors](static/documentation/testing/products-views.webp) | [no errors](static/documentation/testing/products-test-views.webp) | [no errors](static/documentation/testing/products-test-forms.webp) | [no errors](static/documentation/testing/products-tests.webp) |
| Courses  | [no errors](static/documentation/testing/courses-admin.webp) | [no errors](static/documentation/testing/courses-forms.webp) | [no errors](static/documentation/testing/courses-models.webp) | [no errors](static/documentation/testing/courses-urls.webp) | [no errors](static/documentation/testing/courses-views.webp) | [no errors](static/documentation/testing/courses-test-views.webp) | [no errors](static/documentation/testing/courses-test-forms.webp) | [no errors](static/documentation/testing/courses-tests.webp) |

![Python Tests Clear](static/documentation/testing/py-clear.webp)

    NOTE: `settings.py` Stock Django code gives E501 error, left unchanged to keep app from breaking.

![Python Test Settings](static/documentation/testing/settings.webp)

## Lighthouse Test

- [] Desktop view:

    **Home**  
    ![Lighthouse Report Home](static/documentation/testing/lh-home.webp)

    **Grow Kit page**  
    ![Lighthouse Report Review Post Page](static/documentation/testing/lh-products.webp)

    **Grow Guide Page**  
    ![Lighthouse Report About](static/documentation/testing/lh-guide.webp)

    **CoursesPage**  
    ![Lighthouse Report About](static/documentation/testing/lh-courses.webp)

    **Register Page**  
    ![Lighthouse Report Register](static/documentation/testing/lh-signup.webp)

    **Login Page**  
    ![Lighthouse Report Login](static/documentation/testing/lh-login.webp)

    **Logout Page**  
    ![Lighthouse Report Logout](static/documentation/testing/lh-logout.webp)

- [] Mobile view:
    - Performance 

    **Home**  
    ![Lighthouse Report Home Mobile](static/documentation/testing/lh-mobile.webp)

### Accessibility

Accessibility was included in every planning stage for 1up Grow Kits, through the use of the [WAVE report tool](https://wave.webaim.org/) I could ensure that any necessary changes were made to make the website as accessible as it could be.

- 

    ![Errors encountered](static/documentation/testing/errors.webp)

-  [Webaim Contrast Checker](https://webaim.org/resources/contrastchecker/), all errors were resolved successfully.

    ![No errors](static/documentation/testing/clear.webp)  ![Contrast Checker](static/documentation/testing/contrast.webp)


## Manual Testing

### User Input / Form Validation

Testing was carried out on desktop using a Chrome browser to ensure all forms take the intended input and process the input appropriately.
Manual testing by checking the following:

| **TEST INPUT**| **CORRECT OUTCOME** | **MEET REQUIREMENTS** |
| ------------- |:-------------------:|-----------------------|
| **Navbar Logo and Icons** | PASS | Logo takes user to home page, nav bar links take user to intended location, highlight mouse over for better accessibility. Nav bar toggle opens and closes in mobile view | 
| **Login Link** | PASS | Opens Login page |
| **Log into Account** | PASS | Username & password fields. Fields must be exactly as registered originally in either lowercase/uppercase or mixture. Empty fields deliver prompt to user, email field demands '@' symbols. Login is successful, pop up below navbar message to confirm you are logged in.|
| **Register Link** | PASS | Opens Register page |
| **Register Account** | PASS | Username, email(optional) and password fields. Empty fields deliver prompt to user, email field demands '@' symbols, username/password too similar, password too short, username already in use. Account is registered, message to confirm successful sign up |
| **Home Page Shop Now** | PASS | Shop now button directs to the correct products view page |
| **Grow Kits Page Link** | PASS | Grow Kits page loaded |
| **Grow Guide Page Link** | PASS | Grow Guide page loaded |
| **Courses Page Link** | PASS | Courses page loaded |
| **Logout** | PASS | Redirects to log out confirmation page, and user is logged out message confirmed with display as pop up below navbar. |
| **Social Links** | PASS | External link open in a new windows to correct sites |


## Bugs Encountered 
  
The below are bugs that I spent more time investigating, most of these encountered were learning curves. 

| **No.** | **Bug** | **Solved** | **Fix** | **Solution Credit** | **Commit No.** |
| ------- | ------- |:----------:| ------- | ------------------- |:--------------:|
| **1.** | Courses not displaying in bag view | YES | Fix bag logic to handle both Product & Course items. Modified bag_contents to distinguish between items. | [Django Docs](https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/#get-object-or-404/) | 93a69e0 |
| **2.** | Admin OrderLineItem user error | YES | Prevent deleting of line items from the order admin panel, by hiding extra item panels until needed. | [Django Docs](https://docs.djangoproject.com/en/5.1/ref/contrib/admin/) | 44e8f9f |
| **3.**| Delete message prompt in OrderAdmin | YES | Re-activating delete function to modify orders, but prevent deleting accidentally by adding a delete message prompt to admin. Deletion of order items to be confirmed before action proceeds when saved. | [Stack Overflow](https://stackoverflow.com/questions/4661074/delete-confirmation/) | a0bd3de |
| **4.** | Admin OrderLineItem confusing UI logic | YES | Modify product & course fields from side-by-side layout, to a single dropdown field labeled “Item” | [Stack Overflow](https://stackoverflow.com/questions/18265023/self-instance-in-django-modelform/) | e5cb149 |
| **5.** | Course charging delivery cost | NO | xx | xx | xx |

### Unfixed Bugs

- 

    ![Django-Allauth Bug](static/documentation/testing/bug.webp)
