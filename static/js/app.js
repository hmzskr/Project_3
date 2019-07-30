// GET (default method)
fetch('/hello')
     .then(function (response) {
          return response.text();
     }).then(function (text) {
          console.log('GET response text:');
          console.log(text); // Print the greeting as text
     });

// Send the same request
fetch('/hello')
     .then(function (response) {
          return response.json(); // But parse it as JSON this time
     })
     .then(function (json) {
          console.log('GET response as JSON:');
          console.log(json); // Here’s our JSON object
     })

// POST
fetch('/hello', {
     method: 'POST',
     headers: {
          'Content-Type': 'application/json'
     },
     body: JSON.stringify({
          "greeting": "Hello from the browser!"
     })
}).then(function (response) { // At this point, Flask has printed our JSON
     return response.text();
}).then(function (text) {
     console.log('POST response: ');
     // Should be 'OK' if everything was successful
     console.log(text);
});