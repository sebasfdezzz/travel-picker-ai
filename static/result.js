var global_input = "";
let chosen_city="New York";
let cities_result = []; // Assuming this array is declared

function handleCitiesData(citiesData) {
  citiesData.forEach(function (city) {
    cities_result.push(city);

    getUnsplashImageAndUpdate(city);
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

