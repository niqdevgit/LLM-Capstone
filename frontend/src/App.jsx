import { useState } from "react";
import axios from "axios";

function App() {
  const [description, setDescription] = useState("");
  const [xmlResponse, setXmlResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!description) return;

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/generate", {
        description,
      });
      setXmlResponse(response.data); // assuming the backend sends the XML in this format
    } catch (error) {
      console.error("Error while generating IP-XACT component:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (xmlResponse) {
      navigator.clipboard.writeText(xmlResponse);
      alert("XML copied to clipboard");
    }
  };

  return (
    <div className="App">
      <h1>IP-XACT Generator</h1>
      <textarea
        placeholder="Describe your component"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        rows="6"
        cols="50"
      />
      <p></p>
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Generating..." : "Generate IP-XACT"}
      </button>

      {xmlResponse && (
        <div className="xml-response">
          <textarea
            readOnly
            value={JSON.stringify(xmlResponse)}
            rows="10"
            cols="50"
          />
          <p></p>
          <button onClick={handleCopy}>Copy XML</button>
        </div>
      )}
    </div>
  );
}

export default App;
