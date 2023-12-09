console.log("TEST");
var mqtt_server = "test.mosquitto.org";
var mqtt_port = "1883";
var mqtt_destname = "";
let temperatura = 0;
let humidity = 0;
let datastamp="";

//client = new Paho.MQTT.Client("mqtt.hostname.com", Number(8080), "", "clientId");
client = new Paho.MQTT.Client("test.mosquitto.org" ,Number(8080),"","clientId")
//client = new Paho.MQTT.Client("test.mosquitto.org" ,Number(1883),"","clientId")

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});

fetch('http://127.0.0.1:8000/home/db/')
  .then(response => response.json())
  .then(data => showdata(data));  

function showdata(data) {
  for (let r of data) {
    console.log(r.temperatura)
    myChart.data.labels.push(r.datastamp);
    myChart.data.datasets[0].data.push(r.temperatura);
    
    console.log(myChart.data.datasets[0].data.length) 
    if (myChart.data.datasets[0].data.length > 50) {
      myChart.data.labels.shift();
      myChart.data.datasets[0].data.shift();
    }
    myChart.update();
  }
  
}


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription and send a message.
  console.log("onConnect");

  client.subscribe("rasp");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
      console.log("onConnectionLost:"+responseObject.errorMessage);
    }
  }

// called when a message arrives
function onMessageArrived(message) {
    //console.log("onMessageArrived:"+message.payloadString);
    var result = message.destinationName + " : " + message.payloadString + "";
    mes = JSON.parse(message.payloadString);
    console.log(mes)
    
    temperatura = mes['temperatura'];
    humidity = mes['humidity'];
    coolState = mes['CoolState'];
    releState = mes['ReleState'];

    datastamp = mes['datastamp'];


    coolState=(coolState==true)?'ON':'OFF';
    releState=(releState==true)?'ON':'OFF';

    // document.querySelector(".submsg").innerHTML = temperatura; 
    document.getElementById("temperature").innerHTML = temperatura; 
    document.getElementById("humidity").innerHTML = humidity;
    document.getElementById("coolState").innerHTML = coolState;
    document.getElementById("releState").innerHTML = releState;
    document.getElementById("datastamp").innerHTML = datastamp;
    
  

// Тренды
    // showdata(mes)

    myChart.data.labels.push(datastamp);
    myChart.data.datasets[0].data.push(temperatura);
    
    console.log(myChart.data.datasets[0].data.length) 
    if (myChart.data.datasets[0].data.length > 50) {
      myChart.data.labels.shift();
      myChart.data.datasets[0].data.shift();
    }
    myChart.update();
}

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      data: [],
      label: "Total",
      borderColor: "#3e95cd",
      backgroundColor: "#7bb6dd",
      fill: false,
      maxTicksLimit: 10,
    }
    ]
  },
  options: {
    responsive: true,
    title: {
      display: true,
      text: 'Тренды'
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Time'
        },
        ticks: {
          autoSkip: true,
          // maxTicksLimit: 3,
          // max:3,
          // min:3,

          
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Temperature'
        },
        ticks: {
          beginAtZero: true,
          stepSize: 25,
          
        }
      }]
    }
  }
});