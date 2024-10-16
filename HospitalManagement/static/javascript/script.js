document.getElementById('patient-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const disease = document.getElementById('disease').value;

    fetch('/add-patient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, age, disease })
    })
    .then(response => response.text())
    .then(data => {
        console.log(data);
        loadPatients();
        this.reset();
    });
});

function loadPatients() {
    fetch('/patients')
        .then(response => response.json())
        .then(data => {
            const patientList = document.getElementById('patients');
            patientList.innerHTML = '';
            data.forEach(patient => {
                const li = document.createElement('li');
                li.textContent = `${patient.name}, Age: ${patient.age}, Disease: ${patient.disease}`;
                patientList.appendChild(li);
            });
        });
}

document.addEventListener('DOMContentLoaded', loadPatients);

