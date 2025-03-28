document.getElementById("scrapeBtn").addEventListener("click", () => {
    const searchLink = document.getElementById("search_link").value;
    const maxResults = parseInt(document.getElementById("max_results").value);

    chrome.cookies.get({ url: "https://www.linkedin.com", name: "li_at" }, function (cookie) {
        if (cookie) {
            const liAtValue = cookie.value;

            fetch("http://127.0.0.1:8000/scrape/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    li_at: liAtValue,
                    search_link: searchLink,
                    max_results: maxResults
                })
            })
            .then(response => response.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "linkedin_profiles.csv";
                a.style.display = "none";
                document.body.appendChild(a);
                a.click();
                a.remove();
                URL.revokeObjectURL(url); // nettoyage
            })
            .catch(err => {
                document.getElementById("result").textContent = JSON.stringify({ error: err.toString() }, null, 2);
            });
        } else {
            document.getElementById("result").textContent = JSON.stringify({ error: "li_at cookie not found!" }, null, 2);
        }
    });
});
