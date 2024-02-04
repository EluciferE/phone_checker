function checkPhone() {
    const phoneInput = document.getElementById('phoneInput');
    const resultDiv = document.getElementById('result');
    const phoneNumber = phoneInput.value;

    if (!phoneNumber) {
        resultDiv.innerHTML = '';
        resultDiv.className = '';
        return;
    }

    fetch(`/api/v1/phone_info?phone=${encodeURIComponent(phoneNumber)}`)
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `<p>${data.data.message}</p>`;
            let message;
            if (data.status === 'error') {
                resultDiv.className = 'result-error';
                resultDiv.innerHTML = `<p>Ошибка: ${data.data.phone[0]}</p>`;

            } else {
                resultDiv.className = 'result-ok';
                resultDiv.innerHTML = `<p>Номер: ${data.data.phone}</p>
                                        <p>Оператор: ${data.data.operator}</p>
                                        <p>Регион: ${data.data.region}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = 'Произошла непредвиденная ошибка. Попробуйте позже';
            resultDiv.className = 'result-error';
        });
}
