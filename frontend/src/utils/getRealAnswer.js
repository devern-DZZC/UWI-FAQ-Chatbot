export default async function getRealAnswer(question) {
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
  
      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      return data.answer || "Sorry, I couldn't find an answer.";
    } catch (err) {
      console.error(err);
      return "There was an error contacting the server.";
    }
  }
  