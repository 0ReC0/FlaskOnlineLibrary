from __future__ import print_function
from flask import url_for


def test_page_urls(client):
    # Visit home page
    response = client.get(url_for('main.home_page'), follow_redirects=True)
    assert response.status_code == 200

    # Login as user and visit User page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='user@example.com', password='Password1'))
    assert response.status_code == 200

    # Edit User Profile page
    response = client.get(url_for('main.user_profile_page'), follow_redirects=True)
    assert response.status_code == 200

    # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert response.status_code == 200

    # Login as admin and visit Admin page
    response = client.post(url_for('user.login'), follow_redirects=True,
                           data=dict(email='admin@example.com', password='Password1'))
    assert response.status_code == 200
    response = client.get(url_for('book.add_book'), follow_redirects=True)
    assert response.status_code == 200

    # Logout
    response = client.get(url_for('user.logout'), follow_redirects=True)
    assert response.status_code == 200
