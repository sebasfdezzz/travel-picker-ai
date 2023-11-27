console.log("hello world")



async function submitForm() {
    var userInput = document.getElementById('textInput').value;

    try {
        const processResponse = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: userInput }),
        });

        if (processResponse.ok) {
            const processResult = await processResponse.json();

            const cities = processResult.result;
            global_input = userInput;
            window.location.href = '/result?cities=' + encodeURIComponent(JSON.stringify(cities));
        } else {
            console.error('Error:', processResponse.status);
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}


