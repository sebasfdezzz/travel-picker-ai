var global_input = "";
let chosen_city="New York";
let cities_result = []; // Assuming this array is declared

function handleCitiesData(citiesData) {
    chosen_city = citiesData[0];
  citiesData.forEach(function (city) {
    cities_result.push(city);

    getUnsplashImageAndUpdate(city);
    getGptReason(chosen_city);
        // Get all radio buttons with the name "position"
        var radioButtons = document.querySelectorAll('input[name="position"]');

        // Add a click event listener to each radio button
        radioButtons.forEach(function (radio, index) {
            radio.addEventListener('click', function () {
                // The index variable contains the position (1-5) of the clicked radio button
                console.log("Selected position: " + (index + 1));
                chosen_city = cities_result[index];
                getGptReason(chosen_city);
            });
        });
  });
}

function getUnsplashImageAndUpdate(city) {
  fetch(`/get_image/${city}`)
    .then(response => response.json())
    .then(data => {
      updateImageAndLabel(city, data.image_url);
    })
    .catch(error => {
      console.error('Error fetching Unsplash image:', error);
    });
}

function updateImageAndLabel(city, imageUrl) {
  const cityIndex = cities_result.indexOf(city);

  if (cityIndex !== -1) {
    const imageElement = document.querySelector(`#imageCarousel .item:nth-child(${cityIndex + 1}) img`);
    const labelElement = document.querySelector(`#imageCarousel .item:nth-child(${cityIndex + 1}) label`);

    imageElement.src = imageUrl;
    labelElement.textContent = city;
  }
}

function goToKayak() {
    if (airports.hasOwnProperty(chosen_city)) {
      let kayakLink = `https://www.kayak.com.mx/flights/MEX-${airports[chosen_city]}/2024-01-01/2024-01-31-flexible-calendar-6to8?sort=bestflight_a`;
      
      window.location.href = kayakLink;
    } else {
      console.error("Airport code not found for the chosen city");
    }
}


function getGptReason() {

    fetch('/reason-to-go/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ input: global_input, city: chosen_city }),
    })
    .then(response => response.json())
    .then(data => {
      // Update the content of the <p> element with the generated reason
      document.getElementById('reasonParagraph').textContent = data.generated_reason;
    })
    .catch(error => {
      console.error('Error getting reason:', error);
      // Handle error if needed
    });
  }

