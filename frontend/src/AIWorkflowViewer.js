import React, { useState } from "react";
import ReactFlow, { MiniMap, Controls, Background } from "reactflow";
import "reactflow/dist/style.css";

const AIWorkflowViewer = () => {
  const [nodes, setNodes] = useState([
    { id: "1", data: { label: "Start", input: "", output: "" }, position: { x: 250, y: 5 } },
    { id: "2", data: { label: "Input Analysis", input: "", output: "" }, position: { x: 100, y: 100 } },
    { id: "3", data: { label: "Content Generation", input: "", output: "" }, position: { x: 400, y: 100 } },
    { id: "4", data: { label: "AI Handoff", input: "", output: "" }, position: { x: 250, y: 200 } },
    { id: "5", data: { label: "Finalization", input: "", output: "" }, position: { x: 250, y: 300 } },
  ]);

  const fetchAIResponse = async () => {
    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: "Explain how AI improves workflow automation in business." }),
      });

      const data = await response.json();
      console.log("🔹 AI Response Received:", data);

      setNodes((prevNodes) =>
        prevNodes.map((node) =>
          node.id === "3" // Assuming Content Generation node updates
            ? { ...node, data: { label: "Content Generation ✅", input: data.input, output: data.output } }
            : node
        )
      );
    } catch (error) {
      console.error("❌ Error fetching AI response:", error);
    }
  };

  return (
    <div style={{ width: "100vw", height: "100vh", position: "relative" }}>
      <button onClick={fetchAIResponse} style={{ position: "absolute", top: 20, left: 20, padding: "10px" }}>
        Get AI Response
      </button>

      <ReactFlow nodes={nodes} edges={[]} fitView>
        <MiniMap />
        <Controls />
        <Background color="#aaa" gap={16} />
      </ReactFlow>

      <div style={{ position: "absolute", top: 20, right: 20, width: "350px", background: "white", padding: 10, borderRadius: 5, overflowY: "auto", maxHeight: "90vh" }}>
        <h3>AI Execution Details</h3>
        {nodes.map((node) => (
          <div key={node.id} style={{ marginBottom: 15, padding: 10, border: "1px solid #ddd", borderRadius: 5 }}>
            <strong>{node.data.label}</strong>
            {node.data.input && <p>📝 <b>Input:</b> {node.data.input}</p>}
            {node.data.output && (
              <div>
                <p>✅ <b>Output:</b></p>
                <pre style={{ whiteSpace: "pre-wrap", wordWrap: "break-word", background: "#f8f8f8", padding: "5px", borderRadius: "5px" }}>
                  {node.data.output}
                </pre>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default AIWorkflowViewer;
