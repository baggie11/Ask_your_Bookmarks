const askBtn = document.getElementById("askBtn");
const refreshBtn = document.getElementById("refreshBtn");
const questionBox = document.getElementById("question");
const responseDiv = document.getElementById("response");

const BACKEND_URL = "http://localhost:8000";

// === Recursively extract all bookmark URLs from folders ===
function extractUrls(nodes, urls = []) {
  for (let node of nodes) {
    if (node.url) {
      urls.push(node.url);
    }
    if (node.children) {
      extractUrls(node.children, urls);
    }
  }
  return urls;
}

askBtn.addEventListener("click", async () => {
  const question = questionBox.value.trim();
  if (!question) {
    alert("Please enter a question");
    return;
  }

  responseDiv.textContent = "Thinking...";

  chrome.bookmarks.getTree(async (bookmarkTreeNodes) => {
    const rootNodes = bookmarkTreeNodes[0].children; // Fix: go into children of root
    const urls = extractUrls(rootNodes);

    try {
      const res = await fetch(`${BACKEND_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, bookmarks: urls }),
      });

      const data = await res.json();

      if (data.matching_urls && data.matching_urls.length > 0) {
        responseDiv.innerHTML = `
          <p>🔎 Found the following matching bookmarks:</p>
          <ul>
          ${data.matching_urls.map(url => `<li><a href="${url}" target="_blank" style="color: #99ccff;">${url}</a></li>`).join("")}

          </ul>
        `;
      } else {
        responseDiv.textContent = "❌ No relevant content found.";
      }
    } catch (err) {
      console.error(err);
      responseDiv.textContent = "❌ Error getting matching URLs.";
    }
  });
});

refreshBtn.addEventListener("click", () => {
  responseDiv.textContent = "Refreshing bookmark index...";

  chrome.bookmarks.getTree(async (bookmarkTreeNodes) => {
    const rootNodes = bookmarkTreeNodes[0].children; // Fix: go into children of root
    const urls = extractUrls(rootNodes);

    try {
      const res = await fetch(`${BACKEND_URL}/refresh_index`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bookmarks: urls }),
      });

      const data = await res.json();
      responseDiv.textContent = data.status || "✅ Bookmarks indexed!";
    } catch (err) {
      console.error(err);
      responseDiv.textContent = "❌ Failed to refresh index.";
    }
  });
});
