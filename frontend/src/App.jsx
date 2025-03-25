import { useState } from "react";
import axios from "axios";

function App() {
  const [description, setDescription] = useState("");
  const [xmlResponse, setXmlResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [validationStatus, setValidationStatus] = useState(null); // New state for validation status

  const handleSubmit = async () => {
    if (!description) return;

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5000/generate", {
        description,
      });

      setXmlResponse(response.data.generated_text || ""); // Store generated text
      setValidationStatus(response.data.k2xml); // Update validation status
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
    <div className="App" style={{ paddingLeft: "30px" }}>
      <h1>IP-XACT Generator</h1>
      <p>Please note that Hugging Face API needs to "wake up"</p>
      <p>So first request will likely fail, try again in 30 seconds</p>
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

      {/* Validation Status */}
      {validationStatus !== null && (
        <p style={{ color: validationStatus ? "green" : "red" }}>
          {validationStatus
            ? "Kakctus2 validation success"
            : "Kakctus2 validation failed"}
        </p>
      )}

      {xmlResponse && (
        <div className="xml-response">
          <textarea
            readOnly
            value={xmlResponse}
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
