import requests
import csv
import streamlit as st
import io
from login import show_login

def get_user_secuid(username):
    url = "https://tiktok-api23.p.rapidapi.com/api/user/info"
    
    querystring = {"uniqueId": username}
    
    headers = {
        "x-rapidapi-key": "e095c79235msh5b6a8ced9205f47p174637jsnb96f106bb797",
        "x-rapidapi-host": "tiktok-api23.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        secuid = data.get('userInfo', {}).get('user', {}).get('secUid', 'secUid not found')
        return secuid
    else:
        return None

def get_user_followers(secuid):
    url = "https://tiktok-api23.p.rapidapi.com/api/user/followers"
    followers = []
    min_cursor = 0
    
    headers = {
        "x-rapidapi-key": "e095c79235msh5b6a8ced9205f47p174637jsnb96f106bb797",
        "x-rapidapi-host": "tiktok-api23.p.rapidapi.com"
    }
    
    querystring = {"secUid": secuid, "count": "50", "minCursor": str(min_cursor), "maxCursor": "0"}
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        followers.extend(data.get('userList', []))
    
    return followers

def create_csv(followers_list):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['User ID', 'Unique ID', 'Link'])
    writer.writerows(followers_list)
    return output.getvalue()

st.title("TikTok Followers Fetcher")

# Check login status
if not st.session_state.logged_in:
    show_login()

# Main content
if st.session_state.logged_in:
    username = st.text_input("Enter TikTok username:")

    if st.button("Get Followers"):
        secuid = get_user_secuid(username)
        if secuid:
            st.write(f"secUid for {username}: {secuid}")
            followers_data = get_user_followers(secuid)
            if followers_data:
                followers_list = []
                for user in followers_data:
                    user_id = user['user'].get('id')
                    unique_id = user['user'].get('uniqueId')
                    link = f"https://www.tiktok.com/@{unique_id}"
                    followers_list.append([user_id, unique_id, link])

                st.write("Followers data:")
                st.table(followers_list[:50])  # Display only the first 50 followers

                # Create a CSV and provide a download link
                csv_data = create_csv(followers_list[:50])
                st.download_button(
                    label="Download Followers CSV",
                    data=csv_data,
                    file_name='followers.csv',
                    mime='text/csv'
                )

                st.success("Followers data has been written to 'followers.csv'.")
            else:
                st.error("Failed to retrieve followers data.")
        else:
            st.error("Failed to retrieve secUid.")
else:
    st.write("Please log in to access the application.")
