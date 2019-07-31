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
d3.select('#citysubmit').on('click', cityAndOptions)

// fetch function to post city input & return category list & zipcodes via flask from the Yelp API
function cityAndOptions() {
     
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
          let optionsList = response.json()
          return optionsList          
     
     // callback function once result is returned to generate category list for multi-select options
     }).then(function (optionsList) {
          console.log('POST response: ');

          // vars to split the optionsList returned into separate arrays for categories & zip codes
          let categoryList = optionsList[0] 
          let zipCodeList = optionsList[1]                   

          // sets vars to empty arrays to build selection lists
          let categoryOutput = '';
          let zipCodeOutput = '';

          // loop to build category list and append to DOM
          for (i=0; i < categoryList.length; i++) {
               categoryOutput += `<li>${categoryList[i]}</li>`
          }     
          document.getElementById('select-options').innerHTML = categoryOutput;
          
          // loop to build zip code list and append to DOM
          for (i=0; i < zipCodeList.length; i++) {
               zipCodeOutput += `<li>${zipCodeList[i]}</li>`
          }
          document.getElementById('zip-codes').innerHTML = zipCodeOutput;
     })
     // catch any errors that result from the Yelp API call
     .catch(function(err) {
          document.getElementById('select-options').innerHTML = `<p>Yelp's API had a brainfart. Reload the page & try again!</p>`;
     })
}