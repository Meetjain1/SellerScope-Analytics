mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]\n\
primaryColor = \"#4285F4\"\n\
backgroundColor = \"#121212\"\n\
secondaryBackgroundColor = \"#1E1E1E\"\n\
textColor = \"#FFFFFF\"\n\
\n\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
