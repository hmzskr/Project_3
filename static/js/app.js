// GET (default method) - dummy code for testing
fetch('/hello')
     .then(function (response) {
          return response.text();
     }).then(function (text) {
          console.log('GET response text:');
          console.log(text); // Print the greeting as text
     });

// Send the same request - dummy code for testing
fetch('/hello')
     .then(function (response) {
          return response.json(); // But parse it as JSON this time
     })
     .then(function (json) {
          console.log('GET response as JSON:');
          console.log(json); // Here’s our JSON object
     })

// fetch request - dummy code for testing
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

// event handler for the city submit button
d3.select('#citysubmit').on('click', citySelect)

// fetch function to post city input & return category list & zipcodes via flask from the Yelp API
function citySelect() {
     
     d3.event.preventDefault();
     
     // converts city input to variable
     let inputElement = d3.select(".form-control")
     let inputValue = inputElement.property("value");
     
     // fetch request to post city input to flask
     fetch('/citytest', {
          method: 'POST',
          headers: {
               'Content-Type': 'application/json'
          },
          body: JSON.stringify({ inputValue })
     
     // awaits result from Yelp API and converts it to JSON (normally returns as an array)
     }).then(function (response) {          
          let catList = response.json()
          return catList          
     
     // callback function once result is returned to generate category list for multi-select options
     }).then(function (catList) {
          console.log('POST response: ');
          console.log(catList);
          let output = '';
          for (i=0; i < catList.length; i++) {
               output += `<li>${catList[i]}</li>`
          }     
          document.getElementById('select-options').innerHTML = output;
     })
     .catch(function(err) {
          console.log(err)
     })
}