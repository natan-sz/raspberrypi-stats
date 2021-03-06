var temp = document.getElementById("temp");
var therm = document.getElementById("therm");
var fanSlider = document.getElementById("therm")

// Document Element
const body = document.body;

// API URL
const url = "http://192.168.0.75:5000/";


// Polling function gets called every time interval 
function fetchStatus() {
    fetch(url)
    .then(data=>{return data.json()})
    .then(res=>{
        temp.innerHTML = res.temp;
        document.getElementById("uptime").innerHTML = res.uptime;
        document.getElementById("cpu").innerHTML = res.usage.cpu;
		document.getElementById("therm").style.color = `hsl(${120-res.temp},100%,30%)`;
        document.getElementById("cpu").innerHTML = res.usage.cpu;
        document.getElementById("ramUsed").innerHTML = res.usage.memory.used;
        document.getElementById("ramTot").innerHTML = res.usage.memory.total;
        document.getElementById("diskUsed").innerHTML = res.usage.disk.used;
        document.getElementById("diskTot").innerHTML = res.usage.disk.total;
        //document.getElementById("fanSliderSpeed").innerHTML = "Fan Speed: " + res.fanSpeed + "%";
        document.getElementById("fanSpeed").innerHTML =  res.fanSpeed + "%";
		console.log(res);

    });
}

function fetchNexmoStats() {
	fetch(url+"get-nexmo-stats")
	.then(data => {return data.json()})
	.then(res=>{
		let balance = parseFloat(res.balance.value.toFixed(2))
		document.getElementById("nexmoBalance").innerHTML = "£" + balance;
		console.log(res);
	});
}

// Function calls POST request with the desired speed to the /fan-update endpoint
function updateFanSpeed() {
    let newFreq = document.getElementById("fanSlider").value;

    let formData = new FormData();
    formData.append('newFreq', newFreq);
    console.log(formData);

    fetch(url + "fan-update",
        {
            body: formData,
            method: "post"
        });
}

function updateSliderLabel(value) {
    document.getElementById("fanSliderSpeed").innerHTML = "Fan Speed: " + value + "%";
}

window.addEventListener('load', function () {

	document.getElementById("nexmoBalance").innerHTML = `<div class="loader"></div>`

    fetch(url)
    .then(data=>{return data.json()})
    .then(res=>{
        document.getElementById("fanSlider").value = res.fanSpeed;
        document.getElementById("fanSliderSpeed").innerHTML = "Fan Speed: " + res.fanSpeed + "%";
    });

	fetchStatus();
	fetchNexmoStats();

    // Your document is loaded.
    var fetchInterval = 1000; // 1 second.

    // Invoke the request every 1 second.
    setInterval(fetchStatus, fetchInterval);
})
