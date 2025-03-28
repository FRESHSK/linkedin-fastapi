chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scrape") {
        chrome.cookies.get({ url: "https://www.linkedin.com", name: "li_at" }, function(cookie) {
            if (cookie) {
                const liAtValue = cookie.value;

                fetch("http://127.0.0.1:8000/scrape/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        li_at: liAtValue,
                        search_link: request.search_link,
                        max_results: request.max_results
                    })
                })
                .then(response => response.blob())
                .then(blob => {
                    const blobUrl = URL.createObjectURL(blob);
                    chrome.downloads.download({
                        url: blobUrl,
                        filename: "linkedin_profiles.csv",
                        saveAs: true
                    });
                    sendResponse({ success: true });
                })
                .catch(err => {
                    console.error("Error downloading CSV:", err);
                    sendResponse({ error: err.toString() });
                });
            } else {
                sendResponse({ error: "li_at cookie not found!" });
            }
        });

        return true;
    }
});
