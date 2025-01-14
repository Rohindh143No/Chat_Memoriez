from datetime import datetime

def get_file_path():
    return input("Enter the file path of the chat file (e.g., sample.txt): ").strip()

from datetime import datetime

def parse_chat(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    chat_data = []
    participants = set()
    message_counts = {}

    for line in lines:
        # Skip system message lines
        if "Messages and calls are end-to-end encrypted" in line:
            continue
        
        try:
            # Extract timestamp and the rest of the line
            timestamp, rest = line.split(" - ", 1)

            # Try both date formats
            try:
                timestamp = datetime.strptime(timestamp, "%m/%d/%y, %I:%M %p")
            except ValueError:
                timestamp = datetime.strptime(timestamp, "%d/%m/%Y, %I:%M %p")

            # Skip invalid lines without name: message
            if ":" not in rest:
                continue

            # Extract name and message
            name, message = rest.split(": ", 1)
            name = name.strip()
            
            # Collect chat data
            chat_data.append((timestamp, name, message.strip()))
            participants.add(name)
            
            # Count messages
            if name not in message_counts:
                message_counts[name] = 0
            message_counts[name] += 1

        except ValueError:
            continue  # Skip invalid lines

    # Ensure exactly two participants
    if len(participants) != 2:
        raise ValueError("Chat file should have exactly two participants.")

    participants = list(participants)
    return chat_data, participants, message_counts

def generate_html(chat_data, participants, message_counts, output_html):
    with open(output_html, "w", encoding="utf-8") as file:
        file.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{participants[1]}</title>
    <style>
        .message-count {{
            margin: 10px auto;
            font-size: 1.2em;
            text-align: center;
            padding: 15px;
            background: linear-gradient(145deg, #e0e0e0, #ffffff);
            box-shadow: 4px 4px 4px #c0c0c0, -4px -4px 8px aqua;
            border-radius: 10px;
            width: 90%;
            max-width: 400px;
            box-sizing: border-box;
            color: #333;
            font-weight: bold;
        }}

        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }}

        .chat-container {{
            width: 100%;
            max-width: 600px;
            background-color: #37ff30;
            height: 100%;
            max-height: 90vh;
            border: 1px solid #ccc;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            padding: 10px;
            box-sizing: border-box;
        }}

        .message {{
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 10px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}

        .left {{
            align-self: flex-start;
            background-color: #2adefd;
            color: #000;
        }}

        .right {{
            align-self: flex-end;
            background-color: #db2580;
            color: #fff;
        }}

        .timestamp {{
            font-size: 0.7em;
            color: #353338;
            text-align: right;
            margin-top: 5px;
        }}

        .date {{
            text-align: center;
            font-size: 0.8em;
            color: #000000;
            margin: 10px 0;
            background-color: #ffffff;
            padding: 2px 4px;
            border-radius: 12px;
            display: inline-block;
            width: fit-content;
            margin-left: auto;
            margin-right: auto;
        }}
        .swap-button {{
            padding: 8px;
            margin-left: 5px;
            font-size: 1em;
            border-radius: 5px;
            cursor: pointer;
            background-color: #555;
            color: white;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }}

        .search-bar-container {{
            display: flex;
            align-items: center;
            padding: 10px;
            background: #15ff00;
            position: sticky;
            top: 0;
            z-index: 100;
            gap:10px;
        }}

        .search-bar {{
            flex-grow: 1;
            padding: 10px;
            font-size: 1em;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}

        .search-bar:focus {{
            outline: none;
            border-color: #15ff00;
            box-shadow: 0 0 5px #15ff00;
        }}

        .arrow-button {{
            margin-left: 10px;
            padding: 10px;
            font-size: 1em;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }}

        .arrow-button:disabled {{
            background-color: #cccccc;
            cursor: not-allowed;
        }}

        .highlight {{
            background-color: yellow;
        }}
        
        .scroll-to-bottom-button {{
            padding: 10px;
            font-size: 1em;
            background-color: black;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}

        .scroll-to-bottom-button:hover {{
            background-color: white;
            color:black;
        }}

        .scroll-to-top-button {{
            padding: 10px;
            font-size: 1em;
            background-color: black;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            
    
        }}

        .scroll-to-top-button:hover {{
            background-color: white;
            color:black;
        }}

    </style>
</head>
<body>
    <div class="chat-container">
        <div class="search-bar-container">
            <input type="text" id="search-bar" class="search-bar" placeholder="Search messages...">
            <button class="arrow-button" id="arrow-up" onclick="navigateSearch('up')">↑</button>
            <button class="arrow-button" id="arrow-down" onclick="navigateSearch('down')">↓</button>
            <button class="scroll-to-bottom-button" id="scroll-to-bottom-btn">↓</button>
            <button class="scroll-to-top-button" id="scroll-to-top-btn">↑</button>
        </div>
        <div class="message-count">
            <p>Total Messages: {len(chat_data)}</p>
            <p>{participants[0]}: {message_counts[participants[0]]} messages</p>
            <p>{participants[1]}: {message_counts[participants[1]]} messages</p>
        </div>
        
        <div>
            <button class="swap-button" onclick="swapParticipants()">Swap</button>
        </div>
""")
        last_date = None
        for timestamp, name, message in sorted(chat_data, key=lambda x: x[0]):
            current_date = timestamp.strftime("%d/%m/%Y")
            if current_date != last_date:
                file.write(f"""
        <div class="date">{current_date}</div>
""")
                last_date = current_date

            alignment = "right" if name == participants[0] else "left"
            file.write(f"""
        <div class="message {alignment}" data-name="{name}" data-message="{message}">
            <div>{message}</div>
            <div class="timestamp">{timestamp.strftime('%I:%M %p')}</div>
        </div>
""")

        file.write("""        
    </div>
            
    </div>
    <script>
        let searchIndex = -1;
        let searchResults = [];

        document.getElementById("search-bar").addEventListener("input", function () {
            let input = this.value.toLowerCase();
            let messages = document.querySelectorAll(".message");
            searchResults = [];
            searchIndex = -1;

            messages.forEach((message, index) => {
                let text = message.innerText.toLowerCase();
                message.classList.remove("highlight");
                if (text.includes(input) && input) {
                    searchResults.push(index);
                }
            });

            if (searchResults.length > 0) {
                searchIndex = 0;
                highlightSearchResult();
            }
        });

        function navigateSearch(direction) {
            if (searchResults.length === 0) return;

            searchResults.forEach((index) => {
                document.querySelectorAll(".message")[index].classList.remove("highlight");
            });

            if (direction === "up") {
                searchIndex = (searchIndex - 1 + searchResults.length) % searchResults.length;
            } else if (direction === "down") {
                searchIndex = (searchIndex + 1) % searchResults.length;
            }

            highlightSearchResult();
        }

        function highlightSearchResult() {
            if (searchIndex === -1) return;
            let messages = document.querySelectorAll(".message");
            let targetIndex = searchResults[searchIndex];

            messages[targetIndex].classList.add("highlight");
            messages[targetIndex].scrollIntoView({ behavior: "smooth", block: "center" });
        }

        function swapParticipants() {
            let chatContainer = document.querySelector(".chat-container");
            let messageCounts = document.querySelector(".message-count");
            let messages = Array.from(document.querySelectorAll(".message"));

            let countParagraphs = messageCounts.querySelectorAll("p");
            [countParagraphs[1].textContent, countParagraphs[2].textContent] = 
                [countParagraphs[2].textContent, countParagraphs[1].textContent];

            messages.forEach(message => {
                if (message.classList.contains("left")) {
                    message.classList.remove("left");
                    message.classList.add("right");
                } else if (message.classList.contains("right")) {
                    message.classList.remove("right");
                    message.classList.add("left");
                }
            });
        }

        document.getElementById("scroll-to-bottom-btn").addEventListener("click", function () {
            document.querySelector(".chat-container").scrollTo(0, document.querySelector(".chat-container").scrollHeight);
        });

        document.getElementById("scroll-to-top-btn").addEventListener("click", function () {
            document.querySelector(".chat-container").scrollTo(0, 0);
        });
    </script>
</body>
</html>
""")

def main():
    file_path = get_file_path()
    try:
        chat_data, participants, message_counts = parse_chat(file_path)
        output_html = participants[1] + ".html"
        generate_html(chat_data, participants, message_counts, output_html)
        print(f"Responsive HTML chat view generated: {output_html}")
        print(f"Participants identified: {participants[0]} (right), {participants[1]} (left)")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
