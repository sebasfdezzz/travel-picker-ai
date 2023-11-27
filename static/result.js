cities_result = [];
var global_input = "";
function handleCitiesData(citiesData) {
    citiesData.forEach(function(city) {
        cities_result.push(city);
    });
    console.log(cities_result);
}


