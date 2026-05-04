from playwright.sync_api import sync_playwright
import os

html_content = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { background-color: #1e1e1e; color: #d4d4d4; font-family: 'Consolas', 'Courier New', monospace; padding: 20px; font-size: 14px;}
  .keyword { color: #569cd6; }
  .string { color: #ce9178; }
  .function { color: #dcdcaa; }
  .comment { color: #6a9955; }
</style>
</head>
<body>
<pre>
<span class="comment"># Extract from app.py: Groq API Call</span>
<span class="keyword">try</span>:
    completion = client.chat.completions.create(
        model=<span class="string">"llama-3.3-70b-versatile"</span>,
        messages=[
            {<span class="string">"role"</span>: <span class="string">"system"</span>, <span class="string">"content"</span>: system_prompt},
            {<span class="string">"role"</span>: <span class="string">"user"</span>, <span class="string">"content"</span>: user_prompt}
        ],
        temperature=<span class="keyword">0.2</span>,
        max_tokens=<span class="keyword">800</span>
    )
    
    reply = completion.choices[<span class="keyword">0</span>].message.content
    
    <span class="keyword">return</span> {
        <span class="string">'answer'</span>: reply,
        <span class="string">'mode'</span>: matches[<span class="keyword">0</span>][<span class="string">'mode'</span>],
        <span class="string">'confidence'</span>: matches[<span class="keyword">0</span>][<span class="string">'similarity'</span>],
        <span class="string">'method'</span>: <span class="string">'groq_braintrust'</span>
    }
<span class="keyword">except</span> Exception <span class="keyword">as</span> e:
    <span class="function">print</span>(<span class="string">f"⚠️ Neural Link Error (Groq): {e}"</span>)
</pre>
</body>
</html>
"""

with open("api_code.html", "w", encoding="utf-8") as f:
    f.write(html_content)

def capture():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        
        # Capture API code snippet
        page1 = browser.new_page(viewport={"width": 800, "height": 450})
        page1.goto(f"file://{os.path.abspath('api_code.html')}")
        page1.screenshot(path="q12_api_call.png")
        
        # Capture Chatbot UI
        page2 = browser.new_page(viewport={"width": 1280, "height": 720})
        page2.goto("http://127.0.0.1:7860")
        page2.wait_for_timeout(2000)
        page2.fill('textarea', 'What is the fee for BTech CSE?')
        # To press the button, we need to locate it or press Enter
        page2.keyboard.press('Shift+Enter') # in case shift+enter is new line, actually let's click the send button
        try:
            page2.locator("button.send-btn").click()
        except:
            pass
        page2.wait_for_timeout(5000)
        page2.screenshot(path="q13_chatbot_ui.png")
        
        browser.close()

if __name__ == '__main__':
    capture()
