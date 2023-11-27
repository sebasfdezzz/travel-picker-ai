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

            const resultResponse = await fetch('/result', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cities: cities }),
            });

            if (resultResponse.ok) {
                const resultResult = await resultResponse.text();
                console.log(resultResult);
            } else {
                console.error('Error:', resultResponse.status);
            }
        } else {
            console.error('Error:', processResponse.status);
        }
    } catch (error) {
        console.error('Error:', error.message);
    }
}

