// Function to send a POST request with the PDF file and a prompt
async function submitPDF() {
    // Create a FormData object
    const formData = new FormData();

    // Get the file input element and prompt from HTML
    const fileInput = document.getElementById("pdfFile");  // Assuming there's an input with id="pdfFile"
    const prompt = "I have uploaded my medical report. Please provide a summary.";

    // Check if a file was selected
    if (fileInput.files.length === 0) {
        console.error("No file selected.");
        return;
    }

    // Append the file and the prompt to the FormData object
    formData.append("file", fileInput.files[0]);  // The first selected file
    formData.append("prompt", JSON.stringify(prompt));  // Assuming the prompt structure

    // Send the POST request to your chatbot API
    try {
        const response = await fetch('http://192.168.1.182:8080/pdfchatbot', {
            method: 'POST',
            headers: {
                'Sanctum-Api-Key': 'd135d37c-0758-4b1b-89d3-d0fbecfe96f6',  // Replace with the actual API key
                // Do not set 'Content-Type', fetch will automatically set it to 'multipart/form-data' when sending FormData
            },
            body: formData
        });

        // Parse and log the response
        if (response.ok) {
            const result = await response.json();
            console.log("Response:", result);
            alert("Response: " + JSON.stringify(result));
        } else {
            console.error("Error:", response.status, response.statusText);
            alert("Response: " + JSON.stringify(result));
        }
    } catch (error) {
        console.error("Network Error:", error);
    }
}
