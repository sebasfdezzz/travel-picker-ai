let airports = {
    "Bangkok": "BKK",
    "London": "LHR",
    "Paris": "CDG",
    "Dubai": "DXB",
    "New York": "JFK",
    "Singapore": "SIN",
    "Kuala Lumpur": "KUL",
    "Istanbul": "IST",
    "Tokyo": "HND",
    "Seoul": "ICN",
    "Hong Kong": "HKG",
    "Barcelona": "BCN",
    "Amsterdam": "AMS",
    "Milan": "MXP",
    "Rome": "FCO",
    "Osaka": "KIX",
    "Vienna": "VIE",
    "Shanghai": "PVG",
    "Prague": "PRG",
    "Munich": "MUC",
    "Berlin": "BER",
    "Dublin": "DUB",
    "Sydney": "SYD",
    "San Francisco": "SFO",
    "Los Angeles": "LAX",
    "Toronto": "YYZ",
    "Marrakech": "RAK",
    "Budapest": "BUD",
    "Stockholm": "ARN",
    "Zurich": "ZRH",
    "New Delhi": "DEL",
    "Cairo": "CAI",
    "Mexico City": "MEX",
    "Lisbon": "LIS",
    "Rio de Janeiro": "GIG",
    "Hanoi": "HAN",
    "Bangalore": "BLR",
    "Cape Town": "CPT",
    "Athens": "ATH",
    "Iceland": "KEF",
    "Helsinki": "HEL",
    "Moscow": "SVO",
    "Edinburgh": "EDI",
    "Montreal": "YUL",
    "Vancouver": "YVR",
    "Auckland": "AKL",
    "Seville": "SVQ",
    "Beijing": "PEK",
    "Venice": "VCE",
    "Mumbai": "BOM",
    "Buenos Aires": "EZE",
    "Warsaw": "WAW",
    "Manila": "MNL",
    "Phuket": "HKT",
    "Krakow": "KRK",
    "St. Petersburg": "LED",
    "Cologne": "CGN",
    "Brussels": "BRU",
    "Madrid": "MAD",
    "Doha": "DOH",
    "Abu Dhabi": "AUH",
    "Kolkata": "CCU",
    "Brasília": "BSB",
    "Cancun": "CUN",
    "Nairobi": "NBO",
    "Johannesburg": "JNB",
    "Havana": "HAV",
    "Tel Aviv": "TLV",
    "Bucharest": "OTP",
    "Kiev": "KBP",
    "Oslo": "OSL",
    "Panama City": "PTY",
    "Naples": "NAP",
    "Reykjavik": "KEF",
    "Lima": "LIM",
    "Wellington": "WLG",
    "Amman": "AMM",
    "Zagreb": "ZAG",
    "Ljubljana": "LJU",
    "Brisbane": "BNE",
    "Tbilisi": "TBS",
    "Ankara": "ESB",
    "Dakar": "DKR",
    "Casablanca": "CMN",
    "Kigali": "KGL",
    "Porto": "OPO",
    "Luxembourg City": "LUX",
    "Belfast": "BFS",
    "Guatemala City": "GUA",
    "Caracas": "CCS",
    "Tunis": "TUN",
    "Düsseldorf": "DUS",
    "Gothenburg": "GOT",
    "Rotterdam": "RTM",
    "Birmingham": "BHX",
    "Valletta": "MLA",
    "Jerusalem": "JRS",
    "Manama": "BAH",
    "Phnom Penh": "PNH",
    "Astana": "NQZ",
    "Baku": "GYD",
    "Maputo": "MPM"
  }




let chosen_city="New York";
let cities_result = []; // Assuming this array is declared

function handleCitiesData(citiesData) {
    chosen_city = citiesData[0];
    citiesData.forEach(function (city) {
    cities_result.push(city);

    getUnsplashImageAndUpdate(city);
   
  });
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
      // Open the Kayak link in a new tab
      window.open(kayakLink, '_blank');
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
      body: JSON.stringify({city: chosen_city }),
    })
    .then(response => response.json())
    .then(data => {
      // Update the content of the <p> element with the generated reason
      let content = data.generated_reason['choices'][0]['message']['content'];
      document.getElementById('reasonParagraph').textContent = content;
    })
    .catch(error => {
      console.error('Error getting reason:', error);
      // Handle error if needed
    });
  }

