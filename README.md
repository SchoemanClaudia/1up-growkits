# 1up GrowKits

It's more than just an e-commerce store, it's a gateway to sustainable living, self-sufficiency, and hands-on learning.

We are on a mission to empower people, from hobbyists to urban farmers - by providing premium mushroom grow kits and expert-led courses that bring the magic of mushroom cultivation to homes and businesses.

In a world where people crave organic, homegrown food, our platform offers a seamless, educational, and rewarding experience. Customers can purchase high-quality grow kits, book hands-on courses, and access expert knowledge, all through an intuitive and beautifully designed online store.

1up GrowKits is not just a store, it’s a community-driven movement toward sustainability, self-reliance, and the joy of growing your own food.

Let’s grow together!


Live Link: 

![Screen Mock-up](static/documentation/readme/responsive-mockup.png)


## Overview

1up GrowKits is an e-commerce platform for purchasing mushroom grow kits and educational courses on mushroom cultivation. The website offers a seamless shopping experience, with secure Stripe payments, AWS-backed media hosting, and a scalable e-commerce system. Customers can also subscribe to the Mailchimp newsletter for updates and promotions.

- [x] A modern and user-friendly e-commerce store.
- [x] A dedicated course booking system for scheduled training.
- [x] Secure payment processing via Stripe.
- [x] Admin product management with CRUD functionality.
- [x] AWS S3 for media storage (product images).
- [x] Newsletter subscription integration with Mailchimp.
- [x] Facebook social links in the header and footer.

## Features

__Existing features:__
 
- **User Features:**

  - **Product Listings:** Browse and purchase mushroom grow kits.
  - **Course Registration:** Book educational courses on mushroom cultivation.
  - **Shopping Cart & Checkout:** Add products, update quantity, and proceed to payment.
  - **User Authentication:** Secure login & registration via Django AllAuth.
  - **Order Tracking:** View order history and purchase details.
  - **Newsletter Subscription:** Subscribe to Mailchimp for promotions.


- **Admin Features:**

  - **CRUD Functionality:** Admins can Create, Read, Update, and Delete products & courses.
  - **Stock Alerts** Low stock indicators notify admins when inventory is running low.
  - **Order Management** View, process, and update order statuses.


- **Error Pages:**

  - Redirects users to an error page template set up for relevant error type, and prompts users to return to the home page with 'Go Back to Home' button.



__Future Features__

- **Review Posts:**

  - xxx


## Agile

For the Agile process utilised within Github project board and user stories. Detailing the production process and highlighting issues when they arose. 

### Project Issues

![Issues](static/documentation/readme/issues.webp)

New user stories have been added as the project progressed and based on user feedback during the final testing phase. 

A MOSCOW framework has been utilised. 

**Mo:** 
**S:** 
**C:** 
**oW:** 


## User Stories

User stories were used to keep track of the MOSCOW framework and project MVP as working through the project. 

![Agile](static/documentation/readme/agile.webp)

![User stories](static/documentation/readme/user-stories.webp)

| **USER STORY** | **DETAILS** | **ACCEPTANCE CRITERIA** |
| -------------- | ----------- | ----------------------- |


## Site Testing 

Please see [TESTING.md](TESTING.md) document.


## UX/UI Wireframing

- **Key wireframes include:**
  - Landing Page – Featured products & promotions.
  - Product Page – Individual product details & "Add to Cart" button.
  - Cart & Checkout – Item list, total price, and Stripe integration.
  - Course Booking Page – Available courses with dates and registration.
  - Admin Panel – CRUD functionality for product & order management.

### Wireframe

![Wireframe](static/documentation/readme/wireframe.webp)

### UI Colour Palette

![UI Colour Palette](static/documentation/readme/colours.webp)

### User Experience

__User Feedback__

Site was deployed after all styling and error handling was in place. An up-to-date URL was sent to a small group of users to gather feedback on navigation, layout structure, and potential issues they might encounter as while working through the site. 
- This feedback was actioned and added for better user experience.

  - Users were asked to:
    - [x] xxxx


| **FEEDBACK** | **ACTION** | **OUTCOME** |
| ------------ | ---------- | ----------- |


## Solution Model

- **Primary Models:**
  - UserProfile – Stores customer details.
  - Product – Represents grow kits.
  - Course – Represents educational events.
  - Order – Stores product & course purchases.
  - Cart – Handles shopping cart items.
  - Payment – Processes transactions.
  - StockAlert – Tracks low inventory alerts.
  - NewsletterSubscription – Manages email opt-ins for Mailchimp.


### ERD Design

A detailed ERD diagram below to visualize data flow.

![ERD Design](static/documentation/readme/erd.webp)

### Database Model

![Database Model](static/documentation/readme/model.webp)


## Technologies Used

### Languages

__Application Structure__

- **Frontend:**
  - HTML5/CSS3: Provides structure and styling for reviews and user interactions.
  - Bootstrap: Responsive design for easy navigation on various screen sizes.
  - JavaScript: Enhances interactivity (dynamically toggling comments visibility).

- **Backend:**
  - Django Framework (Python): Handles routing, user authentication etc.
  - Stripe API – Secure payment processing.
  - PostgreSQL – Relational database.

### Libraries & Frameworks

- 

### Other Sites

- Testing & Validation
  - HTML: https://validator.w3.org/nu/
  - CSS: https://jigsaw.w3.org/css-validator/#validate_by_uri
  - JavaScript: https://jshint.com/
  - Python: https://pep8ci.herokuapp.com/
  - Accessibility: https://wave.webaim.org/

- Responsive Screen Preview
  - MockUp Generator: https://websitemockupgenerator.com/

- Images downloaded under licensed user
  - Adobe Stock: https://stock.adobe.com/

- Turning FontAwesome icon into sized favicons
  - Favicon: https://favicon.io/

- Contrast checker for accessibility:
  - Webaim: https://webaim.org/
    
- Image assets reduced with online platforms
  - TinyPNG: https://tinypng.com/
  - Bulk Sizing: https://imageresizer.com/bulk-resize/
  - Reduce Images: https://www.reduceimages.com/

- Assisted problem solving sites:
  - 


## Django Project Setup


## Deployment


## Credits 

- Stock Images (licensed):
  - 
