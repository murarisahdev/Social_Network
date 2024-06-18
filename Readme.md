# Social Network App

Social Network App is built with Python-DRF.

## Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/murarisahdev/Social_Network.git
    ```

2. Navigate to the project directory:

    ```bash
    cd social_network
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

5. Run the application:

    ```bash
    docker-compose up --build
    ```
6. Stop application:

    ```bash
    docker-compose down
    ```

#### User Management

- **Register User**
  - Method: POST
  - URL: `/api/register/`
  - Description: Register a new user.

- **Login**
  - Method: POST
  - URL: `/api/login/`
  - Description: Authenticate and log in a user.

- **Search Users**
  - Method: GET
  - URL: `/api/search/`
  - Description: Search users by name or email.

#### Friend Requests

- **Send Friend Request**
  - Method: POST
  - URL: `/api/friend-request/create/`
  - Description: Send a friend request to another user.

- **Accept-Reject Friend Request**
  - Method: PUT
  - URL: `/api/friend-request/2/update/`
  - Description: Accept or Reject a friend request.

- **List Pending Friend Requests**
  - Method: GET
  - URL: `/api/friend-request/pending/`
  - Description: Retrieve a list of pending friend requests received.

- **List Accepted Friend Requests**
  - Method: GET
  - URL: `/api/friend-request/accepted/`
  - Description: Retrieve a list of accepted friend requests.