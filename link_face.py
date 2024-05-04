import streamlit as st
import requests


def extract_https_links(data):
    https_links = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                https_links.extend(extract_https_links(value))
            elif isinstance(value, list):
                for item in value:
                    https_links.extend(extract_https_links(item))
            elif isinstance(value, str) and (value.startswith("http") or value.startswith("https")):
                https_links.append(value)
    elif isinstance(data, list):
        for item in data:
            https_links.extend(extract_https_links(item))
    return https_links


def display_images(https_links):
    if https_links:
        st.subheader("Images from HTTPS links:")
        for link in https_links:
            try:
                st.image(link, caption=link, use_column_width=True)

            except Exception as e:
                st.error(f"Error displaying image from URL: {link}. Error: {str(e)}")
    else:
        st.warning("No HTTPS links found in the JSON data.")


def main():
    st.title("Show Images from JSON Data")

    url = st.text_input("Enter URL of Google Drive JSON file:")
    if st.button("Show"):
        if url:
            try:
                # file_id = url.split("/")[-2]
                # download_url = f"https://drive.google.com/uc?id={file_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    https_links = extract_https_links(data)
                    display_images(https_links)
                else:
                    st.error(f"Failed to retrieve JSON data from URL: {url}. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred while fetching JSON data from URL: {url}. Error: {str(e)}")


if __name__ == "__main__":
    main()
